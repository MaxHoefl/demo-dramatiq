from pydantic import BaseSettings, RedisDsn, validator


class Settings(BaseSettings):
    DB_URL: str
    REDIS_URL: RedisDsn

    class Config:
        env_file = ".env"
        env_prefix = 'DEMO_'

    @validator("DB_URL")
    def replace_postgres_scheme(cls, url: str) -> str:
        """
        Ensures scheme is compatible with newest version of SQLAlchemy.
        Ref: https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
        """
        assert url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    @validator("REDIS_URL")
    def check_redis_url(cls, url: str) -> str:
        assert url
        return url



settings = Settings()