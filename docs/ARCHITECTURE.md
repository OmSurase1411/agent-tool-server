# System Architecture

## Overview

This system is a **modular, MCP-governed Agentic AI architecture** that separates:

* Decision making (LLM)
* Execution (Tools)
* Knowledge (RAG)

---

## High-Level Flow

```
User
 ↓
FastAPI Route (/agent/run)
 ↓
ContextManager (MCP rules)
 ↓
RAG Retrieval (knowledge_base)
 ↓
LLM (Ollama)
 ↓
Decision JSON (MCP schema)
 ↓
Tool Execution (if required)
 ↓
Unified Response
 ↓
Frontend
```

---

## Component Breakdown

### 1. Agent Router (`agent.py`)

* Entry point: `/agent/run`
* Handles:

  * user input
  * RAG retrieval
  * LLM invocation
  * tool execution
* Acts as the **orchestrator**

---

### 2. Context Manager (`context_manager.py`)

* Builds the system prompt
* Enforces MCP rules
* Controls:

  * output format
  * tool usage logic
  * RAG priority

---

### 3. LLM Client (`llm_client.py`)

* Communicates with Ollama
* Sends prompt → receives response
* No business logic inside

---

### 4. Knowledge Base (`knowledge_base/`)

#### Components:

* `loader.py`

  * Loads documents from `/documents`

* `chunker.py`

  * Splits text into overlapping chunks
  * Adds metadata:

    * chunk_id
    * source

* `retriever.py`

  * Keyword-based retrieval
  * Returns top relevant chunks

#### Documents:

* `vehicle_policy.md`
* `customer_support.md`

---

### 5. Tools Layer (`tools.py`)

Deterministic APIs:

* add
* echo
* customer_lookup
* vehicle_info
* uppercase

Characteristics:

* No randomness
* Strict input validation
* Safe execution

---

### 6. MCP Decision Layer

LLM output:

```json
{
  "intent": "...",
  "tool_called": true/false,
  "tool_name": "...",
  "final_response": "..."
}
```

This ensures:

* predictable execution
* structured control
* no ambiguity

---

### 7. Frontend (`frontend.html`)

* Displays:

  * explanations
  * tool outputs
* Hides:

  * raw JSON
  * backend complexity

---

## RAG Integration

```
User Query
 ↓
retrieve_chunks()
 ↓
Relevant Knowledge
 ↓
Injected into Prompt
 ↓
LLM uses it for grounded response
```

---

## Design Principles

### 1. Separation of Concerns

* LLM → decision
* Tools → execution
* RAG → knowledge

---

### 2. Determinism

* No random outputs
* Predictable system behavior

---

### 3. Safety

* No hallucinated tools
* Input validation enforced

---

### 4. Observability

* Raw LLM output logged
* Easy debugging

---

## Key Insight

This architecture reflects real enterprise AI systems where:

* LLMs do NOT act freely
* Everything is governed, validated, and controlled
