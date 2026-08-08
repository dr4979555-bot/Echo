import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import Agent, Post

from schemas.agent import FeedPost, FeedResponse



router = APIRouter(
    prefix="/api/agent",
    tags=["Feed"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/feed",
    response_model=FeedResponse
)
def get_feed(
    agentId: str,
    db: Session = Depends(get_db)
):

    agent = (
        db.query(Agent)
        .filter(Agent.agent_id == agentId)
        .first()
    )

    if not agent:
        return FeedResponse(posts=[])

    posts = (
        db.query(Post)
        .filter(Post.agent_id == agentId)
        .order_by(Post.created_at.desc())
        .all()
    )

    result = []

    for post in posts:

        try:
            sources = json.loads(post.sources) if post.sources else []
        except json.JSONDecodeError:
            sources = []

        result.append(
            FeedPost(
                id=str(post.id),
                createdAt=post.created_at.isoformat() + "Z",
                text=post.content,
                rationale=post.rationale,
                sources=sources
            )
        )

    return FeedResponse(posts=result)

