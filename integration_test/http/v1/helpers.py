from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

import requests
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from config import get_settings
from integration_test.http.v1.constants import LOGIN_PATH
from pkg.infrastructure.datastore import postgres
from pkg.models.base import Base
from pkg.models.factories import connection

__ENGINE: Optional[Engine] = None


def get_authenticated_payload(username: str, password: str) -> Dict[str, Any]:
    return requests.post(
        LOGIN_PATH, json={"username": username, "password": password}
    ).json()


def get_token(username: str, password: str) -> str:
    return get_authenticated_payload(username, password).get("access_token", "")


def _get_engine() -> Engine:
    global __ENGINE
    if __ENGINE is not None:
        return __ENGINE

    settings = get_settings()
    __ENGINE = postgres.get_engine(settings.DATABASE_URL, 1)
    return __ENGINE


def __clear_db(session: Session) -> None:
    session.execute(
        "TRUNCATE {} RESTART IDENTITY CASCADE;".format(
            ",".join(
                f'"{table.name}"' for table in reversed(Base.metadata.sorted_tables)
            )
        )
    )
    session.commit()


@contextmanager
def session_context(
    *args: Any, **kwargs: Any  # noqa: ANN401
) -> Generator[Session, None, None]:
    clear = bool(kwargs.pop("_clear", True))
    with connection.configure_engine(_get_engine()):
        session = connection.get_session(*args, **kwargs)
        try:
            yield session
        finally:
            if clear:
                __clear_db(session)
            connection.get_factory_session().remove()
