from fastapi import APIRouter, Depends

from database.database import get_db
from services.news_service import NewsService
from agents.orchestrator import Orchestrator


router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"]
)


@router.post("/run")
def run_agent(
    agentId: str,
    db=Depends(get_db)
):

    news_service = NewsService()

    orchestrator = Orchestrator(
        news_service,
        db
    )

    result = orchestrator.run(
        agentId
    )

    return result