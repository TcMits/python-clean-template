from typing import Optional

from pydantic import BaseSettings, PostgresDsn

__SETTINGS: Optional["Settings"] = None


class Settings(BaseSettings):
    # postgres
    DATABASE_URL: PostgresDsn
    POOL_SIZE: int = 100

    # gunicorn
    GUNICORN_BIND_ADDR: str = "0.0.0.0:8080"
    GUNICORN_WORKERS: int = 1
    GUNICORN_THREADS: int = 2
    GUNICORN_RELOAD: bool = False

    # login usecase
    LOGIN_USECASE_SECRET: str = "dummy"


def get_settings() -> Settings:
    global __SETTINGS
    if __SETTINGS is None:
        __SETTINGS = Settings()
    return __SETTINGS.copy()
