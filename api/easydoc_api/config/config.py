import os

from pydantic import BaseSettings, Field


class DBConfig(BaseSettings):
    host: str
    port: int = Field(default=5432)
    user: str
    password: str
    db_name: str


def get_db_config() -> DBConfig:
    return DBConfig(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', 5432),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db_name=os.getenv('DB_NAME')
    )


class AppConfig(BaseSettings):
    ai_client_id: str = Field(default=os.getenv('AI_CLIENT_ID'))
    ai_client_secret: str = Field(default=os.getenv('AI_CLIENT_SECRET'))
    db_config: DBConfig = Field(default_factory=get_db_config)


app_config = AppConfig()
