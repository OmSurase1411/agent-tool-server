# 🚀 Agentic AI Tool Server – MCP Governed + RAG-Enabled Agent

This project is a **production-style Agentic AI system** built using **FastAPI** and a local LLM (**Ollama – LLaMA 3**).

It demonstrates how to transform an LLM from a **chatbot into a deterministic system controller** using:

* Model Context Protocol (MCP)
* Tool orchestration
* Retrieval-Augmented Generation (RAG)
* Enterprise-safe decision logic

---

# 🔥 What This Project Does

The agent can:

* Understand user intent
* Decide whether a tool is required
* Execute backend tools deterministically
* Answer knowledge-based questions using **RAG (documents)**
* Return structured JSON responses (MCP enforced)
* Handle missing inputs gracefully (VIN / Customer ID)
* Avoid hallucinations through strict governance

> ❌ Not a chatbot
> ✅ Controlled AI decision system

---

# 🧠 Core Concept: Model Context Protocol (MCP)

MCP is a strict contract that governs LLM behavior.

Every response must follow:

```json id="z7k8xa"
{
  "intent": "string",
  "tool_called": true or false,
  "tool_name": "string or null",
  "final_response": "string"
}
```

### Rules enforced:

* JSON-only output
* No markdown or extra text
* No trailing commas
* Only allowed tool names
* Deterministic behavior
* `final_response` must always exist

👉 This converts the LLM into a **system controller instead of a chatbot**

---

# 🧠 Week 6: RAG (Knowledge Base Integration)

The system integrates a **document-driven knowledge base**.

Instead of relying only on LLM knowledge, the agent retrieves answers from:

* structured policy documents
* controlled enterprise knowledge

---

## 📁 Knowledge Base

```bash id="wdl8fw"
src/knowledge_base/
 ├── documents/
 │   ├── vehicle_policy.md
 │   └── customer_support.md
 ├── loader.py
 ├── chunker.py
 ├── retriever.py
 └── test_rag.py
```

---

## 🔁 RAG Flow

```text id="7bo4o5"
User Query
   ↓
Document Loader
   ↓
Chunking (with metadata)
   ↓
Retriever (keyword-based)
   ↓
Context Injection
   ↓
LLM (MCP controlled)
   ↓
Structured JSON Output
```

---

## 🧠 Behavior

| Query Type         | Behavior               |
| ------------------ | ---------------------- |
| Policy / Knowledge | Answer using documents |
| Action request     | Call tools             |
| Missing input      | Ask politely           |
| Unknown            | Safe fallback          |

---

# 🏗️ System Architecture

```text id="z3o4hw"
User
 ↓
Agent Router (/agent/run)
 ↓
ContextManager (MCP rules + RAG injection)
 ↓
LLM (Ollama)
 ↓
Decision JSON
 ↓
Tool Execution (if required)
 ↓
Final Response
 ↓
Frontend
```

---

# ⚙️ Components

| Component            | Role                           |
| -------------------- | ------------------------------ |
| `agent.py`           | Orchestrates RAG + tools + LLM |
| `context_manager.py` | Enforces MCP rules             |
| `llm_client.py`      | Handles LLM calls              |
| `tools.py`           | Deterministic APIs             |
| `knowledge_base/`    | RAG system                     |
| `frontend.html`      | UI layer                       |

---

# 🛠️ Available Tools

| Tool            | Description                       |
| --------------- | --------------------------------- |
| add             | Adds two numbers                  |
| echo            | Echoes user input                 |
| customer_lookup | Fetches customer details          |
| vehicle_info    | Fetches vehicle details using VIN |
| uppercase       | Converts text to uppercase        |

---

# 🧪 Example Behavior

### ✅ Knowledge Query (RAG)

**Input:**

```
Can I access customer data without ID?
```

**Output:**

```json id="6m2hrq"
{
  "intent": "data_access",
  "tool_called": false,
  "tool_name": null,
  "final_response": "Customer data must be handled according to internal policies..."
}
```

---

### ✅ Tool Execution

**Input:**

```
Add 5 and 10
```

**Output:**

```json id="zlb3sf"
{
  "intent": "calculation",
  "tool_called": true,
  "tool_name": "add",
  "final_response": "Calculating the result."
}
```

---

# 🖥️ Frontend Behavior

The frontend:

* Displays explanations for knowledge queries
* Formats tool outputs cleanly
* Handles validation errors
* Hides raw JSON from users

---

# 🚀 How to Run

### 1. Start Ollama

```bash id="w19b5p"
ollama serve
```

### 2. Pull model

```bash id="5p7eaq"
ollama pull llama3
```

### 3. Start backend

```bash id="h48y1z"
uvicorn src.main:app --reload
```

### 4. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

# 📁 Project Structure

```bash id="g0hrj3"
docs/
 ├── MCP.md
 └── ARCHITECTURE.md

src/
 ├── knowledge_base/
 │   ├── documents/
 │   ├── chunker.py
 │   ├── loader.py
 │   ├── retriever.py
 │   └── test_rag.py
 │
 ├── routes/
 │   ├── agent.py
 │   ├── context_manager.py
 │   ├── llm_client.py
 │   ├── schemas.py
 │   └── tools.py
 │
 ├── config.py
 ├── errors.py
 ├── logger.py
 ├── main.py
 └── frontend.html
```

---

# 🧭 Project Progress

| Week     | Focus                     | Status |
| -------- | ------------------------- | ------ |
| Week 1–2 | FastAPI + Tools           | ✅      |
| Week 3–4 | Agent Logic               | ✅      |
| Week 5   | MCP Governance            | ✅      |
| Week 6   | RAG Integration           | ✅      |
| Week 7   | Workflow Automation (n8n) | 🔜     |

---

# 🎯 Why This Project Matters

This project demonstrates:

* Deterministic AI agent design
* MCP-based LLM governance
* Tool-based execution systems
* Knowledge grounding via RAG
* Separation of:

  * Decision (LLM)
  * Action (Tools)
  * Knowledge (RAG)

👉 This reflects **real-world enterprise AI architecture**

---

# 👥 Collaboration

* Branch + Pull Request workflow
* No direct commits to main
* Multi-developer contribution

---

# 🚀 Next Steps

* Workflow automation (n8n)
* Embedding-based retrieval
* Source attribution
* Multi-agent systems

---

# ⭐ Final Note

This is not a chatbot.

It is a **controlled, explainable, enterprise-grade AI system**.
