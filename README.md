# Minimal Customer Support Agent

A lightweight, production-ready customer support agent built in Python with strong engineering foundations.

This project demonstrates how to build an AI-powered system that is **secure, resilient, and observable** from day one.

---

## 🚀 Features

### 1. Prompt Templates as Code

* Prompts are stored in **YAML** (`prompts.yaml`)
* Version-controlled via Git
* Enables safe iteration and prompt tuning

### 2. Prompt Injection Defense (3-Layer Model)

* **Layer 1:** Pattern-based blocking (e.g. "ignore instructions")
* **Layer 2:** Input validation (length, structure)
* **Layer 3:** Sanitization (cleaning inputs before use)

### 3. Robust Error Handling

* Automatic retries with exponential backoff
* Handles:

  * Rate limits
  * Timeouts
  * Transient failures

### 4. Circuit Breaker

* Prevents cascading failures
* States:

  * `CLOSED` → normal operation
  * `OPEN` → stop calls after repeated failures
  * `HALF_OPEN` → test recovery

### 5. Structured Logging + Cost Tracking

* Logs stored as JSON for easy parsing
* Tracks approximate token usage and cost
* Enables observability and monitoring

## 🔐 Security Principles

* Add `.env` to your `.gitignore` file
* `.env` must **not be committed**
* Store API keys securely using environment variables

Example `.gitignore` entry:

```
.env
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo_url>
cd project
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Configure Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How To Run

```bash
python app.py
```
---

