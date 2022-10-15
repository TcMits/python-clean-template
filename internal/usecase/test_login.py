import uuid
from contextvars import ContextVar
from typing import Any, Dict
from unittest.mock import MagicMock

from internal.usecase.login import LoginUseCase
from pkg import password
from pkg.exceptions import TranslatableException
from pkg.jwt import create_token
from pkg.models.user import User
from pkg.schemas.login import LoginInput

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


def test_loginusecase_login():
    user = User(
        id=uuid.uuid4(),
        is_active=True,
        jwt_token_key=str(uuid.uuid4()),
        username="foofoofoo",
        email="foo@gmail.com",
        password=password.get_hashed_password("12345678"),
    )
    mock_get = MagicMock(return_value=user)

    class FakeRepository:
        get = mock_get

    uc = LoginUseCase(FakeRepository(), "Dummy")
    try:
        uc.login(
            var,
            LoginInput(
                username=user.username,
                password="123456789",
            ),
        )
    except Exception as e:
        assert isinstance(e, TranslatableException)
    else:
        assert 1 == 0

    uc.login(
        var,
        LoginInput(
            username=user.username,
            password="12345678",
        ),
    )

    assert len(mock_get.call_args.args) == 3
    assert mock_get.call_args.args[0] == var


def test_loginusecase_verify_token():
    user = User(
        id=uuid.uuid4(),
        is_active=True,
        jwt_token_key=str(uuid.uuid4()),
        username="foofoofoo",
        email="foo@gmail.com",
    )
    mock_get = MagicMock(return_value=user)

    class FakeRepository:
        get = mock_get

    uc = LoginUseCase(FakeRepository(), "Dummy")
    token = uc._get_access_token(user)
    u = uc.verify_token(var, token)

    assert user.id == u.id
    assert len(mock_get.call_args.args) == 4
    assert mock_get.call_args.args[0] == var


def test_loginusecase_refresh_token():
    user = User(
        id=uuid.uuid4(),
        is_active=True,
        jwt_token_key=str(uuid.uuid4()),
        username="foofoofoo",
        email="foo@gmail.com",
    )
    mock_get = MagicMock(return_value=user)

    class FakeRepository:
        get = mock_get

    uc = LoginUseCase(FakeRepository(), "Dummy")
    tokens = uc._get_refresh_token(user)
    uc.refresh_token(var, tokens)
    assert len(mock_get.call_args.args) == 4
    assert mock_get.call_args.args[0] == var
