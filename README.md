# Agent Tool Server

An enterprise-style **Agent Tool Server** built with FastAPI that simulates how AI agents interact with real-world backend systems through structured, machine-callable tools.

This project is not just a REST API.
It is an execution environment for AI agents where each endpoint represents a *capability* an agent can call, reason over, and chain with other tools.

The project evolved in two phases:

* **Week 2** → Backend infrastructure & production-ready architecture
* **Week 3** → Agent tool execution layer with mock enterprise tools

---

## What is an Agent Tool Server?

An AI agent does not browse websites.
It calls tools with structured input and receives structured output.

Flow:

```
Agent → Tool Endpoint → Structured Response → Agent Reasoning → Next Action
```

This backend provides exactly that mechanism.

All tools follow a unified response contract so that an agent can reason consistently:

```json
{
  "tool": "tool_name",
  "status": "success | error",
  "input": ...,
  "output": ...,
  "message": "optional"
}
```

An agent can simply do:

* If `status == "success"` → use `output`
* If `status == "error"` → read `message` and recover

This is the foundation of agent orchestration.

---

## Project Structure

```
src/
├── main.py            → App entry point, router registration
├── config.py          → Environment configuration
├── logger.py          → Central logging system
├── errors.py          → Global error handling
├── routes/
│   ├── health.py      → Infrastructure health check
│   ├── ping.py        → System sanity check
│   └── tools.py       → All agent tools
```

---

## Infrastructure Endpoints

### Health Check

`GET /health`

Used by infrastructure and monitoring systems.

Response:

```json
{
  "status": "ok",
  "app": "Agent Tool Server"
}
```

---

### Ping

`GET /ping`

Simple logic sanity check.

Response:

```json
{
  "message": "pong"
}
```

---

## Agent Tools

All agent tools live under:

```
/tools/*
```

They are **POST-only** endpoints and are designed for machines (agents), not browsers.

---

### 1. Echo Tool

Utility tool that reflects input.

`POST /tools/echo`

Request:

```json
{
  "text": "hello"
}
```

Response:

```json
{
  "tool": "echo",
  "status": "success",
  "input": "hello",
  "output": "hello",
  "message": null
}
```

---

### 2. Uppercase Tool

Text transformation tool.

`POST /tools/uppercase`

Request:

```json
{
  "text": "hello"
}
```

Response:

```json
{
  "tool": "uppercase",
  "status": "success",
  "input": "hello",
  "output": "HELLO",
  "message": null
}
```

---

### 3. Time Tool (System Tool)

Provides server environment context.

`POST /tools/time`

Request:
(no body)

Response:

```json
{
  "tool": "time",
  "status": "success",
  "input": null,
  "output": "2026-01-14T20:53:12.456789+00:00",
  "message": null
}
```

---

### 4. Customer Lookup Tool (Mock Enterprise)

Simulates a real enterprise customer service.

`POST /tools/customer_lookup`

Request:

```json
{
  "customer_id": "CUST123"
}
```

Response:

```json
{
  "tool": "customer_lookup",
  "status": "success",
  "input": "CUST123",
  "output": {
    "name": "Rahul Mehta",
    "email": "rahul@example.com",
    "status": "Active"
  },
  "message": null
}
```

Failure:

```json
{
  "tool": "customer_lookup",
  "status": "error",
  "input": "CUST000",
  "output": null,
  "message": "Customer not found"
}
```

---

### 5. Vehicle Info Tool (Mock Enterprise)

Simulates a vehicle information system.

`POST /tools/vehicle_info`

Request:

```json
{
  "vin": "VIN123"
}
```

Response:

```json
{
  "tool": "vehicle_info",
  "status": "success",
  "input": "VIN123",
  "output": {
    "model": "BMW X5",
    "year": 2023,
    "status": "In Service"
  },
  "message": null
}
```

Failure:

```json
{
  "tool": "vehicle_info",
  "status": "error",
  "input": "VIN000",
  "output": null,
  "message": "Vehicle not found"
}
```

---

### 6. Add Tool (Math / Reasoning Tool)

Enables numeric computation for agent reasoning.

`POST /tools/add`

Request:

```json
{
  "a": 5,
  "b": 7
}
```

Response:

```json
{
  "tool": "add",
  "status": "success",
  "input": [5, 7],
  "output": 12,
  "message": null
}
```

---

## Why This Is Agentic

This backend behaves exactly like real agent platforms:

* Tools are atomic
* Tools are deterministic
* Tools are machine-callable
* Tools return structured contracts
* Tools can be chained
* Tools simulate enterprise services

An AI agent could:

1. Call `/tools/customer_lookup`
2. Read customer status
3. Call `/tools/vehicle_info`
4. Perform reasoning
5. Call `/tools/add` or `/tools/time`
6. Continue decision making

This is a real agent execution loop.

---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Activate virtual environment:

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Run server:

```bash
uvicorn src.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger (for testing):

```
http://127.0.0.1:8000/docs
```

> Note: In production, many tools are hidden from Swagger because they are machine-only endpoints.

---

## What This Project Represents

This is no longer a FastAPI demo.

It is:

* An **Agent Tool Server**
* With enterprise-style mock services
* Unified tool contracts
* Production-ready backend structure
* Real-world AI architecture

---

## Authors

**Om Rameshwar Surase and Nidhi Chaubey**
Agentic AI & Backend Systems Engineering


