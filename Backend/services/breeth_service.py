import requests

from core.config import settings


class BreethService:

    def __init__(self):

        self.base_url = settings.BREETH_BASE_URL
        self.api_key = settings.BREETH_API_KEY

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def save_episode(self, content):
        """
        Save meaningful Echo Mind memory to Breeth.
        """

        url = f"{self.base_url}/v1/episodes"

        payload = {
            "content": content
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=3
        )

        print("BREETH SAVE STATUS:", response.status_code)
        print("BREETH SAVE RESPONSE:", response.text)

        response.raise_for_status()

        return response.json()

    def save_topic_memory(
        self,
        agent_id,
        title,
        summary,
        category,
        source,
        decision,
        score
    ):
        """
        Store a structured topic memory in Breeth.
        """

        content = f"""
Echo Mind agent {agent_id} discovered a technology topic.

Topic: {title}

Category: {category}

Source: {source}

Summary: {summary}

Editorial decision: {decision}

Editorial score: {score}

Echo Mind evaluated this topic as relevant to its
AI and technology focused persona.
"""

        return self.save_episode(content.strip())

    def search(self, query, limit=5):
        """
        Search Breeth for relevant previous context.
        """

        url = f"{self.base_url}/v1/search"

        payload = {
            "query": query,
            "limit": limit
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=3
        )

        print("BREETH SEARCH STATUS:", response.status_code)
        print("BREETH SEARCH RESPONSE:", response.text)

        response.raise_for_status()

        return response.json()