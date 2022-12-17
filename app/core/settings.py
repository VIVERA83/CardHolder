import os
from pydantic import BaseSettings, BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Postgres(BaseModel):
    db: str
    user: str
    password: str
    host: str
    port: int

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Log(BaseModel):
    level: str


class Settings(BaseSettings):
    postgres: Postgres
    logging: Log

    class Config:
        env_nested_delimiter = "__"
        env_file = BASE_DIR + "/.env_local"
        enf_file_encoding = "utf-8"
