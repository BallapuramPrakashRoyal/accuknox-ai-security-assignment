"""Data Validation Utilities for CSV User Import.

Validation Approach & Scope:
- Name: Non-empty string (2-100 characters), printable alphabetic characters, hyphens, and apostrophes.
- Email: Practical standard format validation verifying [local_part]@[domain].[tld].
  Limitation Note: Regular expression format validation checks structural syntax only.
  It does not verify domain DNS MX records or confirm mailbox deliverability.
"""

import re
from typing import Optional, Tuple

# Standard practical email format regex pattern
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_\-\.\+]+@[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$"
)

# Valid name pattern: letters, spaces, hyphens, periods, apostrophes (2 to 100 characters)
NAME_REGEX = re.compile(r"^[a-zA-Z\s\.\'\-]{2,100}$")


def validate_name(name: Optional[str]) -> Tuple[bool, str, Optional[str]]:
    """Validate user name.
    
    Returns:
        Tuple of (is_valid: bool, sanitized_name: str, error_message: Optional[str])
    """
    if name is None:
        return False, "", "Name field is null/missing"

    cleaned = name.strip()
    if not cleaned:
        return False, "", "Name cannot be empty or whitespace"

    if len(cleaned) < 2:
        return False, cleaned, "Name must be at least 2 characters long"

    if len(cleaned) > 100:
        return False, cleaned, "Name exceeds maximum length of 100 characters"

    if not NAME_REGEX.match(cleaned):
        return False, cleaned, "Name contains invalid characters (only letters, spaces, hyphens, periods, apostrophes allowed)"

    return True, cleaned, None


def validate_email(email: Optional[str]) -> Tuple[bool, str, Optional[str]]:
    """Validate user email address format.
    
    Returns:
        Tuple of (is_valid: bool, sanitized_email: str, error_message: Optional[str])
    """
    if email is None:
        return False, "", "Email field is null/missing"

    cleaned = email.strip()
    if not cleaned:
        return False, "", "Email cannot be empty or whitespace"

    if len(cleaned) > 254:
        return False, cleaned, "Email exceeds maximum RFC length of 254 characters"

    # Reject consecutive dots or invalid punctuation
    if ".." in cleaned or cleaned.startswith(".") or cleaned.endswith("."):
        return False, cleaned, f"Invalid email syntax (consecutive or leading/trailing dots): '{cleaned}'"

    if not EMAIL_REGEX.match(cleaned):
        return False, cleaned, f"Invalid email format: '{cleaned}'"

    # Normalize to lowercase for consistent database deduplication
    normalized = cleaned.lower()
    return True, normalized, None


def validate_user_row(row_data: dict, row_number: int) -> Tuple[bool, dict, Optional[str]]:
    """Perform holistic row validation."""
    name_key = None
    email_key = None
    for k in row_data.keys():
        if k and k.strip().lower() == "name":
            name_key = k
        elif k and k.strip().lower() == "email":
            email_key = k

    if not name_key or not email_key:
        return False, {}, f"Row {row_number}: Missing required CSV columns ('Name' and 'Email')"

    raw_name = row_data.get(name_key)
    raw_email = row_data.get(email_key)

    name_ok, clean_name, name_err = validate_name(raw_name)
    if not name_ok:
        return False, {}, f"Row {row_number}: {name_err}"

    email_ok, clean_email, email_err = validate_email(raw_email)
    if not email_ok:
        return False, {}, f"Row {row_number}: {email_err}"

    return True, {"name": clean_name, "email": clean_email}, None
