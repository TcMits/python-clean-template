from unittest.mock import MagicMock

import starlette_context
from fastapi import status
from fastapi.testclient import TestClient

from internal.controller.http.v1 import get_handler
from internal.controller.http.v1.login import (
    _get_login_handler,
    _get_refresh_token_handler,
    _get_verify_token_handler,
)
from pkg.schemas.login import JWTAuthenticatedPayload, LoginInput, RefreshTokenInput


def test_login_handler():
    class FakeLoginUseCase:
        pass

    uc = FakeLoginUseCase()
    uc.login = MagicMock(
        return_value=JWTAuthenticatedPayload(
            access_token="1", refresh_key="1", refresh_token="1"
        )
    )
    login_input = LoginInput(username="test12354", password="12345678")

    app = get_handler()
    app.post("/test")(_get_login_handler(LoginInput, JWTAuthenticatedPayload, uc))

    client = TestClient(app)
    resp = client.post("/test", json=login_input.dict())

    assert resp.status_code == status.HTTP_200_OK
    uc.login.assert_called_once_with(
        starlette_context._request_scope_context_storage, login_input
    )


def test_verify_token_handler():
    mock_verify = MagicMock()

    class FakeUser:
        pass

    class FakeLoginUseCase:
        def verify_token(self, ctx, token, *args, **kwargs):
            mock_verify(ctx, token, *args, **kwargs)
            if token == "1":
                return FakeUser()
            return None

    uc = FakeLoginUseCase()

    app = get_handler()
    app.post("/test")(_get_verify_token_handler(uc))

    client = TestClient(app)
    resp = client.post("/test", json={"token": "1"})

    assert resp.status_code == status.HTTP_200_OK
    mock_verify.assert_called_with(
        starlette_context._request_scope_context_storage, "1"
    )

    resp = client.post("/test", json={"token": "2"})

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    mock_verify.assert_called_with(
        starlette_context._request_scope_context_storage, "2"
    )


def test_refresh_token_handler():
    class FakeLoginUseCase:
        pass

    uc = FakeLoginUseCase()
    uc.refresh_token = MagicMock(return_value="1")
    refresh_token_input = RefreshTokenInput(refresh_key="123", refresh_token="123")

    app = get_handler()
    app.post("/test")(_get_refresh_token_handler(RefreshTokenInput, uc))

    client = TestClient(app)
    resp = client.post("/test", json=refresh_token_input.dict())

    assert resp.status_code == status.HTTP_200_OK
    uc.refresh_token.assert_called_once_with(
        starlette_context._request_scope_context_storage, refresh_token_input
    )
