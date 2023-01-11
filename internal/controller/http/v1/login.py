from typing import Callable, Coroutine, Type, TypeVar, Union

import starlette_context
from fastapi import APIRouter, FastAPI, Request, Response, status
from pydantic import BaseModel

from internal.controller.http.v1.request import VerifyTokenRequest
from internal.controller.http.v1.response import RefreshTokenResponse
from internal.usecase.base import LoginUseCase
from pkg.models.base import Base
from pkg.models.user import User
from pkg.schemas.login import JWTAuthenticatedPayload, LoginInput, RefreshTokenInput

# subpath
LOGIN_SUBPATH = "/login"
VERIFY_TOKEN_SUBPATH = "/verify-token"
REFRESH_TOKEN_SUBPATH = "/refresh-token"

# name
LOGIN_ROUTE_NAME = "login"
VERIFY_TOKEN_ROUTE_NAME = "verify_token"
REFRESH_TOKEN_ROUTE_NAME = "refresh_token"

# tag names
LOGIN_TAG_NAME = "login"


ModelType = TypeVar("ModelType", bound=Base)
LoginInputType = TypeVar("LoginInputType", bound=BaseModel)
AuthenticatedPayloadType = TypeVar("AuthenticatedPayloadType", bound=BaseModel)
RefreshTokenInputType = TypeVar("RefreshTokenInputType", bound=BaseModel)


def register_login_controller(
    handler: Union[FastAPI, APIRouter],
    login_use_case: LoginUseCase[
        User, LoginInput, JWTAuthenticatedPayload, RefreshTokenInput
    ],
) -> None:
    handler.post(
        LOGIN_SUBPATH,
        name=LOGIN_ROUTE_NAME,
        response_model=JWTAuthenticatedPayload,
        status_code=status.HTTP_200_OK,
        tags=[LOGIN_TAG_NAME],
    )(_get_login_handler(LoginInput, JWTAuthenticatedPayload, login_use_case))
    handler.post(
        VERIFY_TOKEN_SUBPATH,
        name=VERIFY_TOKEN_ROUTE_NAME,
        status_code=status.HTTP_200_OK,
        tags=[LOGIN_TAG_NAME],
    )(_get_verify_token_handler(login_use_case))
    handler.post(
        REFRESH_TOKEN_SUBPATH,
        name=REFRESH_TOKEN_ROUTE_NAME,
        response_model=RefreshTokenResponse,
        status_code=status.HTTP_200_OK,
        tags=[LOGIN_TAG_NAME],
    )(_get_refresh_token_handler(RefreshTokenInput, login_use_case))


def _get_login_handler(
    login_input_type: Type[LoginInputType],
    authenticated_payload_type: Type[AuthenticatedPayloadType],
    login_use_case: LoginUseCase[
        ModelType, LoginInputType, AuthenticatedPayloadType, RefreshTokenInputType
    ],
) -> Callable[
    [Request, LoginInputType], Coroutine[None, None, AuthenticatedPayloadType]
]:
    async def login(
        _: Request, login_input: login_input_type
    ) -> authenticated_payload_type:
        return login_use_case.login(
            starlette_context._request_scope_context_storage, login_input
        )

    return login


def _get_verify_token_handler(
    login_use_case: LoginUseCase[
        ModelType, LoginInputType, AuthenticatedPayloadType, RefreshTokenInputType
    ],
) -> Callable[[Request, str], Coroutine[None, None, Response]]:
    async def verify_token(
        _: Request, verify_token_input: VerifyTokenRequest
    ) -> Response:
        if (
            login_use_case.verify_token(
                starlette_context._request_scope_context_storage,
                verify_token_input.token,
            )
            is None
        ):
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        return Response(status_code=status.HTTP_200_OK)

    return verify_token


def _get_refresh_token_handler(
    refresh_token_input_type: Type[RefreshTokenInputType],
    login_use_case: LoginUseCase[
        ModelType, LoginInputType, AuthenticatedPayloadType, RefreshTokenInputType
    ],
) -> Callable[
    [Request, RefreshTokenInputType], Coroutine[None, None, RefreshTokenResponse]
]:
    async def refresh_token(
        _: Request, refresh_token_input: refresh_token_input_type
    ) -> RefreshTokenResponse:
        return RefreshTokenResponse(
            token=login_use_case.refresh_token(
                starlette_context._request_scope_context_storage, refresh_token_input
            )
        )

    return refresh_token
