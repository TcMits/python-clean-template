from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware


def get_handler() -> FastAPI:
    return FastAPI(
        middleware=[
            Middleware(
                RawContextMiddleware,
                plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
            ),
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ]
    )
