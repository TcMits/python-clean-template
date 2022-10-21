import uuid
from contextvars import ContextVar
from datetime import timedelta
from typing import Any, Dict

from jwt.exceptions import InvalidTokenError

from internal.repository.base import GetRepository
from internal.usecase.base import LoginUseCase as BaseLoginUseCase
from internal.usecase.error_codes import AUTHENTICATION_ERROR, VALIDATION_ERROR
from internal.usecase.i18n_messages import (
    CAN_NOT_LOGIN_NOW_MESSAGE,
    EXPIRED_SESSION_MESSAGE,
    INVALID_LOGIN_INPUT_MESSAGE,
)
from pkg.exceptions import TranslatableException
from pkg.jwt import create_token, jwt_decode
from pkg.models.user import User
from pkg.password import validate_password
from pkg.schemas.login import JWTAuthenticatedPayload, LoginInput, RefreshTokenInput

ACCESS_TOKEN_TIMEOUT = timedelta(minutes=15)
REFRESH_TOKEN_TIMEOUT = timedelta(days=1)


class LoginUseCase(
    BaseLoginUseCase[User, LoginInput, JWTAuthenticatedPayload, RefreshTokenInput]
):
    def __init__(self, get_repository: GetRepository[User], secret: str) -> None:
        self._get_repository = get_repository
        self.__secret = secret
        super().__init__()

    def _get_user_from_payload(
        self, ctx: ContextVar[Dict[Any, Any]], payload: Dict[str, Any]
    ) -> User:
        id = payload.get("id", "")
        jwt_token_key = payload.get("key", "")
        try:
            uuid_id = uuid.UUID(id)
        except (ValueError, TypeError) as e:
            raise TranslatableException(
                e, EXPIRED_SESSION_MESSAGE, _code=VALIDATION_ERROR
            )

        try:
            user = self._get_repository.get(
                ctx,
                User.id == uuid_id,
                User.is_active == True,  # noqa: E712
                User.jwt_token_key == jwt_token_key,
            )
        except Exception as e:
            raise TranslatableException(
                e, EXPIRED_SESSION_MESSAGE, _code=AUTHENTICATION_ERROR
            )
        return user

    def _get_payload(self, user: User) -> Dict[str, Any]:
        return {
            "id": str(user.id),
            "key": user.jwt_token_key,
            "email": user.email,
        }

    def _get_access_token(self, user: User) -> str:
        try:
            return create_token(
                self._get_payload(user), ACCESS_TOKEN_TIMEOUT, self.__secret
            )
        except InvalidTokenError as e:
            raise TranslatableException(
                e, CAN_NOT_LOGIN_NOW_MESSAGE, _code=VALIDATION_ERROR
            )

    def _get_refresh_token(self, user: User) -> RefreshTokenInput:
        try:
            refresh_key = create_token({}, REFRESH_TOKEN_TIMEOUT, self.__secret)
            refresh_token = create_token(
                self._get_payload(user),
                REFRESH_TOKEN_TIMEOUT,
                self.__secret + refresh_key,
            )
        except InvalidTokenError as e:
            raise TranslatableException(
                e, CAN_NOT_LOGIN_NOW_MESSAGE, _code=VALIDATION_ERROR
            )

        return RefreshTokenInput(refresh_key=refresh_key, refresh_token=refresh_token)

    def _parse_access_token(self, ctx: ContextVar[Dict[Any, Any]], token: str) -> User:
        try:
            payload = jwt_decode(token, self.__secret)
        except InvalidTokenError as e:
            raise TranslatableException(
                e, EXPIRED_SESSION_MESSAGE, _code=VALIDATION_ERROR
            )
        return self._get_user_from_payload(ctx, payload)

    def _parse_refresh_token(
        self, ctx: ContextVar[Dict[Any, Any]], refresh_token_input: RefreshTokenInput
    ) -> User:
        try:
            payload = jwt_decode(
                refresh_token_input.refresh_token,
                self.__secret + refresh_token_input.refresh_key,
            )
        except InvalidTokenError as e:
            raise TranslatableException(
                e, EXPIRED_SESSION_MESSAGE, _code=VALIDATION_ERROR
            )
        return self._get_user_from_payload(ctx, payload)

    def login(
        self, ctx: ContextVar[Dict[Any, Any]], login_input: LoginInput
    ) -> JWTAuthenticatedPayload:
        try:
            user = self._get_repository.get(
                ctx,
                User.username == login_input.username,
                User.is_active == True,  # noqa: E712
            )
        except Exception as e:
            raise TranslatableException(
                e, INVALID_LOGIN_INPUT_MESSAGE, _code=AUTHENTICATION_ERROR
            )

        try:
            if not validate_password(user.password, login_input.password):
                raise TranslatableException(
                    ValueError(
                        "internal.usecase.login.LoginUseCase.Login: invalid password"
                    ),
                    INVALID_LOGIN_INPUT_MESSAGE,
                    _code=AUTHENTICATION_ERROR,
                )
        except (ValueError, TypeError) as e:
            raise TranslatableException(
                e, INVALID_LOGIN_INPUT_MESSAGE, _code=AUTHENTICATION_ERROR
            )

        return JWTAuthenticatedPayload(
            access_token=self._get_access_token(user),
            **self._get_refresh_token(user).dict()
        )

    def verify_token(self, ctx: ContextVar[Dict[Any, Any]], token: str) -> User:
        return self._parse_access_token(ctx, token)

    def refresh_token(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        refresh_token_input: RefreshTokenInput,
    ) -> str:
        user = self._parse_refresh_token(ctx, refresh_token_input)
        return self._get_access_token(user)
