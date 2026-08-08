from core.config import settings


class AIService:

    def __init__(self):
        self.api_key = settings.BREETH_API_KEY

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate AI response.
        Actual Breeth API implementation will be added later.
        """

        raise NotImplementedError(
            "Breeth API integration is not implemented yet."
        )