from fastapi import FastAPI
from sqlalchemy.engine import Engine

from config import Settings
from internal.controller.http.v1 import get_handler
from pkg.infrastructure.datastore import postgres
from pkg.infrastructure.gunicorn import GunicornApplication


def run(project_root: str, settings: Settings):
    _: Engine = postgres.get_engine(settings.DATABASE_URL, settings.POOL_SIZE)
    handler: FastAPI = get_handler()

    http_application: GunicornApplication = GunicornApplication(
        handler=handler,
        options={
            "bind": settings.GUNICORN_BIND_ADDR,
            "workers": settings.GUNICORN_WORKERS,
            "threads": settings.GUNICORN_THREADS,
            "reload": settings.GUNICORN_RELOAD,
            "chdir": project_root,
            "worker_class": "uvicorn.workers.UvicornWorker",
        },
    )
    http_application.run()
