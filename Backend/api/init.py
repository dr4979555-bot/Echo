from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from database.database import SessionLocal
from database.models import Agent

from schemas.agent import (
    AgentInitRequest,
    AgentInitResponse
)


router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/init",
    response_model=AgentInitResponse
)
def initialize_agent(
    request: AgentInitRequest,
    db: Session = Depends(get_db)
):

    agent_id = str(uuid4())

    agent = Agent(
        agent_id=agent_id,
        name=request.persona.name,
        domain=request.persona.domain
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return AgentInitResponse(
        agentId=agent.agent_id
    )