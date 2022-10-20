from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

import requests
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from config import get_settings
from integration_test.http.v1.constants import LOGIN_PATH
from pkg.infrastructure.datastore import postgres
from pkg.models.factories import connection

__ENGINE: Optional[Engine] = None


def get_authenticated_payload(username: str, password: str) -> Dict[str, Any]:
    return requests.post(
        LOGIN_PATH, data={"username": username, "password": password}
    ).json()


def get_token(username: str, password: str) -> str:
    return get_authenticated_payload(username, password).get("access_token", "")


def _get_engine() -> Engine:
    global __ENGINE
    if __ENGINE is not None:
        return __ENGINE

    settings = get_settings()
    __ENGINE = postgres.get_engine(settings.DATABASE_URL, settings.POOL_SIZE)
    return __ENGINE


@contextmanager
def session_context(
    *args: Any, **kwargs: Any  # noqa: ANN401
) -> Generator[None, None, Session]:
    clear = bool(kwargs.get("_clear", True))
    with connection.configure_engine(_get_engine()):
        session = connection.get_session(*args, **kwargs)
        try:
            yield session
        finally:
            if clear:
                session.rollback()
            session.remove()
