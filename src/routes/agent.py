from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import re
from datetime import datetime

agent_router = APIRouter(prefix="/agent", tags=["agent"])

TOOLS_BASE_URL = "http://localhost:8000/tools"


class AgentRequest(BaseModel):
    text: str | None = ""


class AgentResponse(BaseModel):
    query: str
    agent_type: str
    tool_used: str | None
    status: str
    result: dict | None


def build_agent_response(query, tool_name, tool_response):
    return {
        "query": query,
        "agent_type": "rule_based",
        "tool_used": tool_name,
        "status": tool_response.get("status"),
        "result": tool_response
    }


@agent_router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    user_text = (request.text or "").strip()

    async with httpx.AsyncClient() as client:

        # 1️⃣ Empty input → agent-level failure
        if not user_text:
            return {
                "query": "",
                "agent_type": "rule_based",
                "tool_used": None,
                "status": "failed",
                "result": {
                    "message": "Please enter some text"
                }
            }

        # 2️⃣ Echo command
        if user_text.lower().startswith("echo "):
            payload = {"text": user_text[5:]}
            r = await client.post(f"{TOOLS_BASE_URL}/echo", json=payload)
            tool_response = r.json()
            return build_agent_response(user_text, "echo", tool_response)

        # 3️⃣ Add tool (numbers)
        numbers = list(map(int, re.findall(r"-?\d+", user_text)))
        if len(numbers) >= 2:
            payload = {"a": numbers[0], "b": numbers[1]}
            r = await client.post(f"{TOOLS_BASE_URL}/add", json=payload)
            tool_response = r.json()
            return build_agent_response(user_text, "add", tool_response)

        # 4️⃣ Customer lookup
        if "cust" in user_text.lower():
            match = re.search(r"(cust\d+)", user_text.lower())
            if match:
                r = await client.post(
                    f"{TOOLS_BASE_URL}/customer_lookup",
                    json={"customer_id": match.group(1).upper()},
                )
                tool_response = r.json()
                return build_agent_response(user_text, "customer_lookup", tool_response)

        # 5️⃣ Vehicle lookup
        if "vin" in user_text.lower():
            match = re.search(r"(vin\d+)", user_text.lower())
            if match:
                r = await client.post(
                    f"{TOOLS_BASE_URL}/vehicle_info",
                    json={"vin": match.group(1).upper()},
                )
                tool_response = r.json()
                return build_agent_response(user_text, "vehicle_info", tool_response)

        # 6️⃣ Default → Uppercase
        r = await client.post(
            f"{TOOLS_BASE_URL}/uppercase",
            json={"text": user_text},
        )
        tool_response = r.json()
        return build_agent_response(user_text, "uppercase", tool_response)
