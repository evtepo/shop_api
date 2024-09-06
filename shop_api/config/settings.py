from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field("shop_api", alias="PROJECT_NAME")

    local_host: str = Field("localhost", alias="LOCALHOST")
    local_port: int = Field(8000, alias="LOCALPORT")

    db_name: str = Field("shop_api", alias="POSTGRES_DB")
    db_user: str = Field("app", alias="POSTGRES_USER")
    db_password: str = Field("123qwe", alias="POSTGRES_PASSWORD")
    db_host: str = Field("shop_db", alias="POSTGRES_HOST")
    db_port: int = Field(5432, alias="POSTGRES_PORT")



settings = Settings()

postgres_dsn = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
