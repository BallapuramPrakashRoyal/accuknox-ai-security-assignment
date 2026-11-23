"""REST API Client for retrieving book data from Open Library."""

import logging
from typing import Any, Dict, List, Optional, Tuple
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class BookAPIClient:
    """Client for interacting with the public Open Library Search API.
    
    Default behavior: Connects to the genuine external Open Library REST API.
    Offline mode: Explicitly engaged only when requested via allow_fallback=True.
    """

    OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

    # Deterministic reference dataset for documented offline execution
    # Provenance: Curated benchmark of canonical computer security and software engineering textbooks
    FALLBACK_BOOKS: List[Dict[str, Any]] = [
        {"title": "Computer Systems Security: Principles and Practice", "authors": ["William Stallings", "Lawrie Brown"], "publication_year": 2018, "isbn": "9780134794105"},
        {"title": "The Web Application Hacker's Handbook", "authors": ["Dafydd Stuttard", "Marcus Pinto"], "publication_year": 2011, "isbn": "9781118026472"},
        {"title": "Practical Malware Analysis", "authors": ["Michael Sikorski", "Andrew Honig"], "publication_year": 2012, "isbn": "9781593272906"},
        {"title": "Applied Cryptography", "authors": ["Bruce Schneier"], "publication_year": 2015, "isbn": "9781119096726"},
        {"title": "Hacking: The Art of Exploitation", "authors": ["Jon Erickson"], "publication_year": 2008, "isbn": "9781593271442"},
        {"title": "Designing Data-Intensive Applications", "authors": ["Martin Kleppmann"], "publication_year": 2017, "isbn": "9781449373320"},
        {"title": "Clean Architecture: A Craftsman's Guide", "authors": ["Robert C. Martin"], "publication_year": 2017, "isbn": "9780134494166"},
        {"title": "Threat Modeling: Designing for Security", "authors": ["Adam Shostack"], "publication_year": 2014, "isbn": "9781118809990"},
        {"title": "Adversarial Machine Learning", "authors": ["Anthony D. Joseph", "Blaine Nelson", "Benjamin I. P. Rubinstein", "J. D. Tygar"], "publication_year": 2019, "isbn": "9781108473439"},
        {"title": "Security Engineering: A Guide to Building Dependable Distributed Systems", "authors": ["Ross Anderson"], "publication_year": 2020, "isbn": "9781119642787"}
    ]

    def __init__(self, timeout: int = 10, max_retries: int = 2):
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retries for transient HTTP errors
        retries = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({
            "User-Agent": "AccuKnox-Assessment-BookFetcher/2.0 (Candidate: Prakash Royal; Academic Evaluation)"
        })

    def fetch_books(
        self,
        query: str = "cybersecurity",
        limit: int = 8,
        allow_fallback: bool = False
    ) -> Tuple[List[Dict[str, Any]], str]:
        """Fetch book data from Open Library REST API.
        
        Args:
            query: Search query string.
            limit: Maximum number of book records to parse.
            allow_fallback: If True, falls back to local reference dataset on network failure.
                            If False (default), raises the exception on network failure.
            
        Returns:
            Tuple of (parsed_books, data_source_label)
        """
        params = {"q": query, "limit": limit}
        logger.info(f"Connecting to REST API: {self.OPEN_LIBRARY_URL} (query='{query}', limit={limit})")

        try:
            response = self.session.get(self.OPEN_LIBRARY_URL, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            payload = response.json()
            docs = payload.get("docs", [])
            logger.info(f"Received HTTP {response.status_code} with {len(docs)} documents from Open Library.")

            books = self._parse_api_response(docs, limit)
            if not books:
                if allow_fallback:
                    logger.warning("Live API returned 0 matching records; using offline benchmark dataset.")
                    return self.FALLBACK_BOOKS[:limit], "OFFLINE_FALLBACK (0 records returned by API)"
                return [], "LIVE_OPEN_LIBRARY_API (Empty)"

            return books, "LIVE_OPEN_LIBRARY_API"

        except requests.exceptions.RequestException as exc:
            logger.error(f"Live API communication failed: {exc}")
            if allow_fallback:
                logger.info("Engaging documented offline reference dataset fallback.")
                return self.FALLBACK_BOOKS[:limit], f"OFFLINE_FALLBACK ({type(exc).__name__})"
            raise ConnectionError(
                f"Failed to connect to external Open Library REST API: {exc}. "
                f"If testing in an air-gapped or network-restricted environment, pass --offline to use the documented reference dataset."
            ) from exc

        except ValueError as exc:
            logger.error(f"Malformed JSON response from API: {exc}")
            if allow_fallback:
                return self.FALLBACK_BOOKS[:limit], "OFFLINE_FALLBACK (Malformed JSON)"
            raise ValueError(f"Malformed JSON received from Open Library API: {exc}") from exc

    def _parse_api_response(self, docs: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Extract and sanitize title, authors, publication year, and isbn from API payload."""
        parsed_books = []
        for doc in docs:
            title = doc.get("title", "").strip()
            if not title:
                continue

            # Extract multiple authors cleanly
            raw_authors = doc.get("author_name", [])
            if isinstance(raw_authors, list) and raw_authors:
                authors = [a.strip() for a in raw_authors if isinstance(a, str) and a.strip()]
            elif isinstance(raw_authors, str) and raw_authors.strip():
                authors = [raw_authors.strip()]
            else:
                authors = ["Unknown Author"]

            # Extract publication year
            pub_year = doc.get("first_publish_year")
            if not pub_year:
                years = doc.get("publish_year", [])
                pub_year = years[0] if (years and isinstance(years, list)) else None
            
            # Extract first available ISBN if present
            isbns = doc.get("isbn", [])
            isbn = isbns[0].strip() if (isbns and isinstance(isbns, list)) else None

            # Extract stable Open Library work/edition key (e.g. /works/OL12345W)
            ol_key = doc.get("key")
            if ol_key and isinstance(ol_key, str):
                ol_key = ol_key.strip()
            else:
                ol_key = None

            parsed_books.append({
                "title": title,
                "authors": authors,
                "publication_year": int(pub_year) if pub_year else None,
                "isbn": isbn,
                "openlibrary_key": ol_key
            })

            if len(parsed_books) >= limit:
                break

        return parsed_books
