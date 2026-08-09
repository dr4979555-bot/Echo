from datetime import datetime
import json
from html import escape

from database.models import Post


class PublishingEngine:

    def __init__(self, db):
        self.db = db

    def publish(self, topic, rationale):

        agent_id = topic.get("agent_id")

        if not agent_id:
            raise ValueError(
                "agent_id is required for publishing"
            )

        url = topic.get("url")

        post = Post(
            agent_id=agent_id,
            content=self.generate_post(topic),
            rationale=rationale,
            sources=json.dumps(
                [url] if url else []
            ),
            created_at=datetime.utcnow()
        )

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        return post

    def generate_post(self, topic):

        title = escape(
            str(topic.get("title", "")).strip()
        )

        summary = escape(
            str(topic.get("summary", "")).strip()
        )

        url = topic.get("url")
        take = topic.get("take")

        if take:
            take = escape(
                str(take).strip()
            )
        else:
            take = (
                "Echo Mind could not generate a "
                "topic-specific perspective for this story."
            )

        post_content = (
            f"<h3>🚀 {title}</h3>"
            f"<p>{summary}</p>"
            f"<p>"
            f"<strong>Echo Mind's take:</strong> "
            f"{take}"
            f"</p>"
        )

        if url:

            safe_url = escape(
                str(url),
                quote=True
            )

            post_content += (
                f'<p>'
                f'<a href="{safe_url}" '
                f'target="_blank" '
                f'rel="noopener noreferrer">'
                f'🔗 Read Source'
                f'</a>'
                f'</p>'
            )

        return post_content