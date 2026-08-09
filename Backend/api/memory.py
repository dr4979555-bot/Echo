from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from agents.memory_engine import MemoryEngine


router = APIRouter(
    prefix="/api/agent",
    tags=["Memory"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/memory")
def get_memory(
    agentId: str,
    db: Session = Depends(get_db)
):
    memory_engine = MemoryEngine(db)

    memories = memory_engine.get_all_memory(agentId)

    return {
        "memories": [
            {
                "id": memory.id,
                "topic": memory.topic,
                "decision": memory.decision,
                "importanceScore": memory.importance_score,
                "createdAt": memory.created_at.isoformat() + "Z"
            }
            for memory in memories
        ]
    }