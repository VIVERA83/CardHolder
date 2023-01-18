import os
import socket

from pydantic import BaseModel, BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
HOST = socket.gethostbyaddr(socket.gethostname())[-1][0]
PORT = 8000


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
    host: str = HOST
    port: int = PORT

    class Config:
        env_nested_delimiter = "__"
        env_file = BASE_DIR + "/.env_local"
        enf_file_encoding = "utf-8"
