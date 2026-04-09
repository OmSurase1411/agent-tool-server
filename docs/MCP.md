# Model Context Protocol (MCP)

## Overview

The Model Context Protocol (MCP) is a strict control layer that governs how the LLM behaves inside the system.

Instead of acting like a chatbot, the LLM is constrained to behave as a **deterministic decision engine**.

---

## Core Purpose

* Enforce structured outputs
* Prevent hallucinations
* Control tool usage
* Ensure predictable behavior
* Maintain system safety

---

## Output Schema

Every LLM response must follow:

```json
{
  "intent": "string",
  "tool_called": true or false,
  "tool_name": "string or null",
  "final_response": "string"
}
```

---

## Rules Enforced

* JSON-only output (no markdown)
* No trailing commas
* No additional text outside JSON
* Only allowed tool names:

  * echo
  * add
  * customer_lookup
  * vehicle_info
  * uppercase
* `tool_called` must be accurate
* `tool_name` must be null if no tool is used
* `final_response` must never be empty

---

## Decision Logic

The LLM is guided using strict rules:

### 1. Knowledge-based Queries (RAG)

* Policies, guidelines, explanations
* Must NOT call tools
* Must use retrieved knowledge

### 2. Action-based Queries

* Calculations → `add`
* Customer lookup → `customer_lookup`
* Vehicle lookup → `vehicle_info`
* Text transformation → `uppercase`

---

## RAG Integration Rule

If relevant knowledge is provided:

* The LLM MUST prioritize it
* Must not ignore provided context
* Must not hallucinate external information

---

## Why MCP Matters

Without MCP:

* LLM behaves unpredictably
* Hallucinates tool calls
* Produces inconsistent outputs

With MCP:

* Fully controlled decision-making
* Deterministic system behavior
* Enterprise-grade reliability

---

## Key Insight

MCP transforms:

> ❌ Chatbot → unpredictable
> ✅ Agent → controlled system controller
