from pydantic import BaseModel
from typing import List


class Persona(BaseModel):
    name: str
    domain: str


class AgentInitRequest(BaseModel):
    persona: Persona


class AgentInitResponse(BaseModel):
    agentId: str


class FeedPost(BaseModel):
    id: str
    createdAt: str
    text: str
    rationale: str
    sources: List[str]


class FeedResponse(BaseModel):
    posts: List[FeedPost]