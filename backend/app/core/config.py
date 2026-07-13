from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized app configuration, loaded from environment variables (or a .env file).
    Nothing that varies between environments (dev/prod) should be hardcoded elsewhere.
    """

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "bleach_codex"

    gemini_api_key: str = ""
    chroma_persist_dir: str = "./chroma_db"
    allowed_origins: str = ""  # comma-separated extra origins, e.g. your deployed frontend URL

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()