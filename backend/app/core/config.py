from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ---------- Core app ----------
    env: str = "local"
    app_name: str = "Regent Data Rights Orchestrator"
    api_prefix: str = "/"
    debug: bool = True

    # Where the React frontend runs (for CORS)
    frontend_origin: str = "http://localhost:5173"

    # ---------- Primary SQL database ----------
    database_url: str = "sqlite:///./regent.db"

    # ---------- Orchestration ----------
    # "simulation" vs "live" (for future)
    default_mode: str = "simulation"

    # ---------- LLM / Audit Summaries ----------
    # Toggle: if false, system uses fallback templates only.
    llm_enabled: bool = False

    # If you later use a local free model (e.g. Ollama):
    # Example: "http://localhost:11434"
    llm_base_url: str = "http://localhost:11434"

    # Example for Ollama: "llama3.2" or any pulled model
    llm_model_name: str = "llama3.2"

    # ---------- Mongo / ADLS (simulated connectors) ----------
    # These are for demo connectors; they can point to mock data.
    mongo_uri: str = "mongodb://localhost:27017"
    adls_base_path: str = "./mock_adls"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # --------- Backwards-compatible UPPERCASE attributes ---------
    # Old code uses settings.ENV, settings.APP_NAME, settings.DATABASE_URL,
    # settings.MODE, settings.MONGO_URI, settings.ADLS_BASE_PATH,
    # settings.FRONTEND_ORIGIN, etc.

    @property
    def ENV(self) -> str:
        return self.env

    @property
    def APP_NAME(self) -> str:
        return self.app_name

    @property
    def API_PREFIX(self) -> str:
        return self.api_prefix

    @property
    def DEBUG(self) -> bool:
        return self.debug

    @property
    def FRONTEND_ORIGIN(self) -> str:
        return self.frontend_origin

    @property
    def DATABASE_URL(self) -> str:
        return self.database_url

    @property
    def DEFAULT_MODE(self) -> str:
        return self.default_mode

    @property
    def MODE(self) -> str:
        """
        Old code expects settings.MODE (e.g. "SIMULATION").
        We map it to default_mode.
        """
        return (self.default_mode or "simulation")

    @property
    def MONGO_URI(self) -> str:
        """
        Backwards compat: some connectors use settings.MONGO_URI.
        """
        return self.mongo_uri

    @property
    def ADLS_BASE_PATH(self) -> str:
        """
        Backwards compat: ADLS connector uses settings.ADLS_BASE_PATH.
        """
        return self.adls_base_path


@lru_cache
def get_settings() -> Settings:
    return Settings()
