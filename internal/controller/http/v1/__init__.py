from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from internal.controller.http.v1.exceptions import exception_handler
from internal.controller.http.v1.health import register_health_check_controller
from internal.controller.http.v1.login import register_login_controller
from internal.usecase.base import LoginUseCase
from pkg.exceptions import TranslatableException
from pkg.models.user import User
from pkg.schemas.login import JWTAuthenticatedPayload, LoginInput, RefreshTokenInput


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
        ],
        debug=False,
    )


def register_services(
    handler: FastAPI,
    login_use_case: LoginUseCase[
        User, LoginInput, JWTAuthenticatedPayload, RefreshTokenInput
    ],
) -> None:
    router = APIRouter()

    # add exception handlers
    handler.add_exception_handler(Exception, exception_handler)
    handler.add_exception_handler(ValidationError, exception_handler)
    handler.add_exception_handler(RequestValidationError, exception_handler)
    handler.add_exception_handler(StarletteHTTPException, exception_handler)
    handler.add_exception_handler(TranslatableException, exception_handler)

    # register routes
    register_health_check_controller(handler)
    register_login_controller(router, login_use_case)

    handler.include_router(router, prefix="/api/v1")
