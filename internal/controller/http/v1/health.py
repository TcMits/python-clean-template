from typing import Union

from fastapi import APIRouter, FastAPI
from starlette.responses import PlainTextResponse

# sub path
HEALTH_CHECK_SUBPATH = "/ping"

# route names
HEALTH_CHECK_ROUTE_NAME = "health_check"


async def health_check() -> str:
    return "pong"


def register_health_check_controller(handler: Union[FastAPI, APIRouter]) -> None:
    handler.get(
        HEALTH_CHECK_SUBPATH,
        name=HEALTH_CHECK_ROUTE_NAME,
        response_class=PlainTextResponse,
    )(health_check)
