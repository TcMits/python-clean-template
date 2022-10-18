from fastapi import FastAPI
from sqlalchemy.engine import Engine

from config import Settings
from internal.controller.http.v1 import get_handler, register_services
from internal.repository.user import UserGetLoginRepository
from internal.usecase.login import LoginUseCase
from pkg.infrastructure.datastore import postgres
from pkg.infrastructure.gunicorn import GunicornApplication


def run(project_root: str, settings: Settings) -> None:
    engine: Engine = postgres.get_engine(settings.DATABASE_URL, settings.POOL_SIZE)
    handler: FastAPI = get_handler()

    # repositories
    user_get_login_repository = UserGetLoginRepository(engine)

    # usecases
    login_use_case = LoginUseCase(
        user_get_login_repository, settings.LOGIN_USECASE_SECRET
    )

    register_services(handler, login_use_case)

    http_application: GunicornApplication = GunicornApplication(
        handler=handler,
        options={
            "bind": settings.GUNICORN_BIND_ADDR,
            "workers": settings.GUNICORN_WORKERS,
            "threads": settings.GUNICORN_THREADS,
            "reload": settings.GUNICORN_RELOAD,
            "chdir": project_root,
            "worker_class": "uvicorn.workers.UvicornWorker",
            "accesslog": "-",
            "errorlog": "-",
            # uvicorn - access log format is not working https://github.com/benoitc/gunicorn/issues/2299
            "access_log_format": '%(s)s %(M)s %(h)s "%(r)s"',
        },
    )
    http_application.run()
