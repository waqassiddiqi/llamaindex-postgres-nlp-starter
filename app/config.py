import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    azure_api_key: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    embed_model: str = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    postgres_uri: str = os.getenv("POSTGRES_URI")
    max_rows: int = int(os.getenv("MAX_ROWS", "500"))


settings = Settings()