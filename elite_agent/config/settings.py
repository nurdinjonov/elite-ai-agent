"""Centralized settings management using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # Tavily
    tavily_api_key: str = ""

    # ChromaDB
    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection_knowledge: str = "agent_knowledge"
    chroma_collection_memory: str = "agent_long_term_memory"

    # Agent
    agent_name: str = "EliteAgent"
    agent_max_iterations: int = 15
    agent_verbose: bool = True


settings = Settings()
