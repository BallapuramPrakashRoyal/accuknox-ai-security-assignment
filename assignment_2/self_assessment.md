# Assignment 2: Technical Self-Assessment

**Candidate:** Ballapuram Prakash Royal  
**Role Target:** AI Security Engineer Trainee (AccuKnox)  
**Evaluation Standard:** Recruiter Rating Scale:
- **A:** Can code independently.
- **B:** Can code under supervision.
- **C:** Little or no understanding.

## 1. Summary Self-Assessment Matrix

| Domain | Self-Assessment Rating | Project Exposure & Foundation | Practical Capability |
| :--- | :---: | :--- | :--- |
| **Artificial Intelligence (AI)** | **B** | **FlowPilot AI:** Worked with workflow execution logic, agent orchestrator concepts, and state handling.<br>**IMLPTS:** Automated penetration testing lifecycle coordination across crawling, scanning, and simulated attack steps. | Can implement agent workflows, decision logic, and state-machine steps under engineering supervision. |
| **Machine Learning (ML)** | **B** | **IMLPTS:** Preprocessed Kaggle CVE vulnerability records, engineered feature vectors, trained Random Forest classifiers with Scikit-learn, and evaluated precision, recall, and F1 metrics. | Can prepare datasets, extract features, train baseline classifiers, and tune hyperparameters under guidance. |
| **Deep Learning (DL)** | **B** | **IMLPTS:** Implemented Bidirectional LSTM sequence classification in Keras for vulnerability descriptions; worked with Deep Q-Network (DQN) implementation with experience replay for discrete exploit action selection. | Can build and train neural network models, sequence classifiers, and standard reinforcement learning loops under guidance. |
| **Large Language Models (LLM)** | **B** | **FlowPilot AI:** Integrated multi-provider LLM API endpoints (Gemini, Ollama, OpenAI-compatible), prompt construction, and basic vector similarity search for document context retrieval. | Can integrate LLM APIs, construct structured prompt templates, implement RAG retrieval pipelines, and apply output validation under guidance. |

---

## 2. Technical Justification & Practical Project Exposure

### 2.1 Artificial Intelligence (Rating: B — Can code under supervision)
- **Actual Project Exposure:** In *FlowPilot AI*, worked with the application backend to implement execution runners (`runner.py`) and agent routing concepts (`orchestrator.py`). In *IMLPTS*, co-developed the four-phase penetration testing engine (`PenTestEngine`) coordinating crawler outputs, vulnerability scanning, and reinforcement learning decisions.
- **Honest Boundary:** I understand agent planning patterns, Directed Acyclic Graph (DAG) state transitions, and tool-calling flows, but complex multi-agent synchronization and distributed fault tolerance in high-throughput production environments would benefit from senior engineering supervision.

### 2.2 Machine Learning (Rating: B — Can code under supervision)
- **Actual Project Exposure:** In *IMLPTS*, preprocessed tabular data from the Kaggle CVE dataset, handled missing attributes, scaled continuous features using standard scalers, trained a Random Forest model (150 trees, max depth 10) for vulnerability severity classification, and evaluated cross-validated confusion matrices.
- **Honest Boundary:** I have practical experience with Scikit-learn, classical algorithms (Random Forest, Decision Trees, Logistic Regression), and standard evaluation metrics (Precision, Recall, F1-score). Advanced feature engineering across highly unstructured domain data or complex ensemble stacking would be executed under senior supervision.

### 2.3 Deep Learning (Rating: B — Can code under supervision)
- **Actual Project Exposure:** In *IMLPTS*, co-developed a Keras/TensorFlow Bidirectional LSTM (BiLSTM) sequence model with embedding layers and dropout to classify vulnerability description text. Also implemented a Deep Q-Network (DQN) reinforcement learning agent with an experience replay buffer to select tactical penetration testing actions from a discrete action space.
- **Honest Boundary:** I understand backpropagation, vanishing/exploding gradients, recurrent cell mechanisms, and Q-learning Bellman updates. Complex custom loss design, distributed multi-GPU training, or architectural novelties would be carried out with engineering mentorship.

### 2.4 Large Language Models (Rating: B — Can code under supervision)
- **Actual Project Exposure:** In *FlowPilot AI*, implemented API integration layers connecting to commercial and local model endpoints (Gemini, Ollama), structured prompt templates, and basic RAG document chunking and cosine similarity retrieval.
- **Honest Boundary:** I can build functional LLM applications, integrate external tools via function calling schemas, and apply input/output guardrails. Fine-tuning foundation models (LoRA/QLoRA), complex prompt security optimization, and low-latency inference serving at large scale would be performed under technical supervision.
