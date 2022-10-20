from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import orm
from sqlalchemy.engine import Engine

__FACTORY_SESSION = orm.scoped_session(orm.sessionmaker())


@contextmanager
def configure_engine(bind: Engine) -> Generator[None, None, None]:
    global __FACTORY_SESSION

    session_factory: orm.sessionmaker = __FACTORY_SESSION.session_factory
    if session_factory.kw.get("bind", None) is not None:
        raise ValueError("configure_engine doesn't support nested context")

    __FACTORY_SESSION.configure(bind=bind)
    try:
        yield
    finally:
        __FACTORY_SESSION.configure(bind=None)


def get_session(*args: Any, **kwargs: Any) -> orm.scoped_session:  # noqa: ANN401
    global __FACTORY_SESSION

    session_factory: orm.sessionmaker = __FACTORY_SESSION.session_factory
    if session_factory.kw.get("bind", None) is None:
        raise ValueError("get_session can't be called outside configure_engine context")

    return __FACTORY_SESSION(*args, **kwargs)
