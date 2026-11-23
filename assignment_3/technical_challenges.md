# Assignment 3: Why this project was challenging

**Candidate:** Ballapuram Prakash Royal  
**Project:** Intelligent Multi-Layer Penetration Testing System Using Hybrid AI Models (IMLPTS)  
**Research Reference:** [IEEE Xplore Digital Library — Document ID 11518386](https://ieeexplore.ieee.org/document/11518386)  

---

## Technical challenges

> **1. Integrating Random Forest, BiLSTM and Deep Q-Network models was challenging because each model performs a different role within the penetration-testing workflow.**
>
> **2. The system required coordinating vulnerability classification and reinforcement-learning-based decision-making across multiple security assessment stages.**
>
> **3. Evaluating the combined framework was more complex than evaluating individual models because their outputs had to work together to support the overall security assessment.**

---

## Brief Technical Elaboration

### 1. Integrating Three Distinct AI Models
The system uses three models with different data requirements and outputs:
- **Random Forest:** Evaluates tabular vulnerability metrics (access vectors, authentication requirements, impact scores).
- **Bidirectional LSTM:** Processes raw text descriptions of vulnerabilities to capture contextual patterns in natural language.
- **Deep Q-Network (DQN):** Operates on a discrete action space (`[Reconnaissance, SQLi, XSS, CSRF, RCE, Privilege Escalation]`) to learn sequential decision-making.

Connecting these models into a synchronized pipeline required defining consistent data structures so that vulnerability classification outputs could directly inform the state representation used by the reinforcement learning agent.

### 2. Coordination and Data Preprocessing
Combining supervised classification with reinforcement learning meant handling two distinct stages of data processing:
- Preprocessing the CVE dataset involved parsing inconsistent text descriptions, handling missing attributes, and normalizing features for supervised training.
- Designing the custom simulation environment (`PenTestEnv`) required defining a reward structure that provided meaningful feedback to the DQN agent for choosing tactical actions corresponding to identified vulnerabilities.

### 3. System-Level Evaluation
Evaluating the integrated workflow was more involved than standard model benchmarking:
- Evaluating Random Forest or BiLSTM alone relies on standard classification metrics (precision, recall, F1-score).
- Evaluating the combined system required observing whether the DQN agent learned to select appropriate actions in the simulated environment based on the classification priors, and verifying that the entire automated flow—from crawling to report generation—executed reliably without manual intervention.
