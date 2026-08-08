from sqlalchemy.orm import Session
from database.models import Agent, Post, Memory


def create_agent(db: Session, name: str, domain: str):
    agent = Agent(
        name=name,
        domain=domain
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent


def get_agent(db: Session, agent_id: int):
    return db.query(Agent).filter(Agent.id == agent_id).first()


def create_post(db: Session, content, rationale, sources):
    post = Post(
        content=content,
        rationale=rationale,
        sources=sources
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def get_posts(db: Session):
    return (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .all()
    )


def save_memory(db: Session, topic, decision, score):

    memory = Memory(
        topic=topic,
        decision=decision,
        importance_score=score
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory