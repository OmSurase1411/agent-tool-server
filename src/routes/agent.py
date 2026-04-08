from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import json

from src.routes.context_manager import ContextManager
from src.routes.llm_client import LLMClient
from src.routes.schemas import AgentResponse

from src.knowledge_base.loader import load_documents
from src.knowledge_base.chunker import chunk_text
from src.knowledge_base.retriever import retrieve_chunks


# -------------------------------------------------------------------
# Tool name normalization (LLM → Backend)
# -------------------------------------------------------------------

TOOL_ALIASES = {
    "calculator": "add",
    "calc": "add",
    "math": "add",

    "customer finder": "customer_lookup",
    "customer search": "customer_lookup",
    "customer lookup": "customer_lookup",

    "vin decoder": "vehicle_info",
    "vin lookup": "vehicle_info",
    "vehicle lookup": "vehicle_info",
}

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------

agent_router = APIRouter(prefix="/agent", tags=["agent"])

TOOLS_BASE_URL = "http://localhost:8000/tools"

context_manager = ContextManager()
llm_client = LLMClient(model_name="llama3:latest")

# -------------------------------------------------------------------
# LOAD KNOWLEDGE BASE (runs once at startup)
# -------------------------------------------------------------------

docs = load_documents("src/knowledge_base/documents")

ALL_CHUNKS = []

for doc in docs:
    chunks = chunk_text(doc["content"], doc["filename"])
    ALL_CHUNKS.extend(chunks)


# -------------------------------------------------------------------
# Request model
# -------------------------------------------------------------------

class AgentRequest(BaseModel):
    text: str | None = ""


# -------------------------------------------------------------------
# Tool Executor (Single Source of Truth)
# -------------------------------------------------------------------

async def execute_tool(tool_name: str, user_text: str):
    async with httpx.AsyncClient() as client:

        if tool_name == "echo":
            r = await client.post(f"{TOOLS_BASE_URL}/echo", json={"text": user_text})
            return r.json()

        elif tool_name == "add":
            import re
            numbers = list(map(int, re.findall(r"-?\d+", user_text)))
            r = await client.post(
                f"{TOOLS_BASE_URL}/add",
                json={"a": numbers[0], "b": numbers[1]}
            )
            return r.json()

        elif tool_name == "customer_lookup":
            import re
            match = re.search(r"(cust\d+)", user_text.lower())
            if not match:
                return {
                    "status": "failed",
                    "message": "I think you forgot the Customer ID. Please enter something like CUST123."
                }

            r = await client.post(
                f"{TOOLS_BASE_URL}/customer_lookup",
                json={"customer_id": match.group(1).upper()}
            )
            return r.json()

        elif tool_name == "vehicle_info":
            import re
            match = re.search(r"(vin\d+)", user_text.lower())
            if not match:
                return {
                    "status": "failed",
                    "message": "I think you forgot the VIN number. Please enter something like VIN123."
                }

            r = await client.post(
                f"{TOOLS_BASE_URL}/vehicle_info",
                json={"vin": match.group(1).upper()}
            )
            return r.json()

        elif tool_name == "uppercase":
            r = await client.post(
                f"{TOOLS_BASE_URL}/uppercase",
                json={"text": user_text}
            )
            return r.json()

        else:
            return {"error": f"Unknown tool: {tool_name}"}


# -------------------------------------------------------------------
# MCP + LLM governed agent route
# -------------------------------------------------------------------

@agent_router.post("/run")
async def run_agent(request: AgentRequest):
    user_text = (request.text or "").strip()

    if not user_text:
        return {
            "error": "Empty input",
            "message": "Please provide some text"
        }

    # -------------------------------------------------------------------
    # RAG STEP (retrieve relevant knowledge)
    # -------------------------------------------------------------------

    retrieved_chunks = retrieve_chunks(user_text, ALL_CHUNKS)

    context_text = "\n".join([chunk["text"] for chunk in retrieved_chunks])

    # -------------------------------------------------------------------
    # Build MCP prompt + inject knowledge
    # -------------------------------------------------------------------

    prompt = context_manager.build_prompt(user_text)

    if context_text:
        prompt += f"\n\nRelevant Knowledge:\n{context_text}"

    # -------------------------------------------------------------------
    # Call LLM
    # -------------------------------------------------------------------

    raw_response = llm_client.invoke(prompt)

    print("\n====== RAW LLM OUTPUT ======")
    print(raw_response)
    print("====== END RAW OUTPUT ======\n")

    # -------------------------------------------------------------------
    # Parse response
    # -------------------------------------------------------------------

    try:
        parsed = json.loads(raw_response)
        agent_decision = AgentResponse(**parsed)
    except Exception as e:
        return {
            "error": "Invalid LLM response format",
            "raw_output": raw_response,
            "exception": str(e)
        }

    # -------------------------------------------------------------------
    # No tool needed → return
    # -------------------------------------------------------------------

    if not agent_decision.tool_called:
        return agent_decision.dict()

    # -------------------------------------------------------------------
    # Normalize tool name
    # -------------------------------------------------------------------

    tool_name = (
        agent_decision.tool_name.lower().strip()
        if agent_decision.tool_name else ""
    )

    tool_name = TOOL_ALIASES.get(tool_name, tool_name)

    # -------------------------------------------------------------------
    # Execute tool
    # -------------------------------------------------------------------

    tool_result = await execute_tool(tool_name, user_text)

    # -------------------------------------------------------------------
    # Final response
    # -------------------------------------------------------------------

    return {
        "intent": agent_decision.intent,
        "tool_called": True,
        "tool_name": tool_name,
        "final_response": agent_decision.final_response,
        "tool_result": tool_result
    }
