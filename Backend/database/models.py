from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database.database import Base


class Agent(Base):

    __tablename__ = "agents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    agent_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    domain = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Post(Base):

    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    agent_id = Column(
        String,
        nullable=False,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )

    rationale = Column(
        Text,
        nullable=False
    )

    sources = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Memory(Base):

    __tablename__ = "memory"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    agent_id = Column(
        String,
        nullable=False,
        index=True
    )

    topic = Column(
    String,
    nullable=False,
    index=True
   )
    
    decision = Column(
        String,
        nullable=False
    )

    importance_score = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )