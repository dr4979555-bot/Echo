from fastapi import APIRouter, Depends
from pydantic import BaseModel

from database.database import get_db
from database.models import Agent
from services.news_service import NewsService
from agents.orchestrator import Orchestrator


router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"]
)


class AgentRunRequest(BaseModel):
    agent_id: str
    objective: str


@router.post("/run")
def run_agent(
    request: AgentRunRequest,
    db=Depends(get_db)
):
    # Check agent exists
    agent = (
        db.query(Agent)
        .filter(Agent.agent_id == request.agent_id)
        .first()
    )

    if not agent:
        return {
            "success": False,
            "error": "Agent not found",
            "agent_id": request.agent_id
        }

    news_service = NewsService()

    orchestrator = Orchestrator(
        news_service,
        db
    )

    # IMPORTANT:
    # Pass both objective and agent_id
    result = orchestrator.run(
        objective=request.objective,
        agent_id=request.agent_id
    )

    result["success"] = True
    result["agent_id"] = request.agent_id
    result["objective"] = request.objective

    return result