import os

class Settings:
    openai_api_key = os.getenv("")
    postgres_host = os.getenv("POSTGRES_HOST", "ndruznpao5.vw1gkkb5oq.tsdb.cloud.timescale.com")
    postgres_port = int(os.getenv("POSTGRES_PORT", 39912))
    postgres_user = os.getenv("POSTGRES_USER", "tsdbadmin")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "b2dlhwxb3h0b4gqz")
    postgres_db = os.getenv("POSTGRES_DB", "tsdb")
    postgres_db_diy = os.getenv("POSTGRES_DB_DIY", postgres_db)

    # RAG fallback table/column
    search_table = os.getenv("SEARCH_TABLE", "brands")
    search_column = os.getenv("SEARCH_COLUMN", "name")

    cache_ttl_seconds = int(os.getenv("CACHE_TTL_SECONDS", 300))
    use_vector_search = os.getenv("USE_VECTOR_SEARCH", "true").lower() == "true"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    @property
    def postgres_diy_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_db_diy}"
        )

settings = Settings()
