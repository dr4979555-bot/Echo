from datetime import datetime
import json

from database.models import Post


class PublishingEngine:

    def __init__(self, db):
        self.db = db

    def publish(self, topic, rationale):

        post = Post(
            agent_id=topic["agent_id"],
            content=self.generate_post(topic),
            rationale=rationale,
            sources=json.dumps(
                [topic["url"]]
                if topic.get("url")
                else []
            ),
            created_at=datetime.utcnow()
        )

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        return post

    def generate_post(self, topic):

        return (
            f"🚀 {topic['title']}\n\n"
            f"{topic['summary']}\n\n"
            "Echo Mind's take: This development is worth watching "
            "because it could influence the future of AI and technology."
        )