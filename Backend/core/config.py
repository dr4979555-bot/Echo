from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    PROJECT_NAME = "Echo Mind"
    VERSION = "1.0.0"

    BREETH_API_KEY = os.getenv("BREETH_API_KEY")

    BREETH_BASE_URL = os.getenv("BREETH_BASE_URL", "")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./echo_mind.db"
    )


settings = Settings()