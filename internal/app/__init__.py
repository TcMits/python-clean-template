from typing import Optional, Tuple

from fastapi import FastAPI
from sqlalchemy.engine import Engine

from config import Settings
from pkg.infrastructure.datastore import postgres
from pkg.infrastructure.gunicorn import GunicornApplication

__LOAD_CACHE: Optional[Tuple[FastAPI]] = None


def __load(
    _: str, settings: Settings, engine: Engine, *, reload: bool = False
) -> Tuple[FastAPI]:  # add more handlers
    """
    This function create repository, use cases and return pure handlers for application
    """

    global __LOAD_CACHE
    if not reload and __LOAD_CACHE is not None:
        return __LOAD_CACHE

    from internal.controller.http.v1 import get_handler, register_services
    from internal.repository.user import UserGetLoginRepository
    from internal.usecase.login import LoginUseCase

    http_handler: FastAPI = get_handler()

    # repositories
    user_get_login_repository = UserGetLoginRepository(engine)

    # usecases
    login_use_case = LoginUseCase(
        user_get_login_repository, settings.LOGIN_USECASE_SECRET
    )

    register_services(http_handler, login_use_case)

    __LOAD_CACHE = (http_handler,)
    return __LOAD_CACHE


def run(project_root: str, settings: Settings) -> None:
    engine: Engine = postgres.get_engine(settings.DATABASE_URL, settings.POOL_SIZE)
    # you can fork for each handler, but i only have 1 http service now
    # handlers = __load(project_root, settings, engine, reload=False)

    worker_class = "uvicorn.workers.UvicornWorker"
    if settings.GUNICORN_RELOAD:  # set False in production
        # reload does not work for uvicorn.workers.UvicornWorker
        # https://github.com/benoitc/gunicorn/issues/2339
        worker_class = "pkg.infrastructure.worker.uvicorn.RestartableUvicornWorker"

    http_application: GunicornApplication = GunicornApplication(
        lambda: __load(project_root, settings, engine, reload=settings.GUNICORN_RELOAD)[
            0
        ],
        options={
            "bind": settings.GUNICORN_BIND_ADDR,
            "workers": settings.GUNICORN_WORKERS,
            "threads": settings.GUNICORN_THREADS,
            "reload": settings.GUNICORN_RELOAD,
            "reload_engine": "inotify",
            "chdir": project_root,
            "worker_class": worker_class,
            "accesslog": "-",
            "errorlog": "-",
            # uvicorn - access log format is not working
            # https://github.com/benoitc/gunicorn/issues/2299
            "access_log_format": '%(s)s %(M)s %(h)s "%(r)s"',
        },
    )
    http_application.run()
