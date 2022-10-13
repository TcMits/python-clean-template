from contextvars import ContextVar
from typing import Any, Dict
from unittest.mock import MagicMock

from internal.usecase.create import SimpleCreateUseCase

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


def test_simplecreateusecase_create():
    mock_create = MagicMock(return_value=1)
    mock_v = MagicMock(return_value=None)

    class MockCreateRepository:
        create = mock_create

    uc = SimpleCreateUseCase(MockCreateRepository(), mock_v)
    assert uc.create(var, None)
    mock_v.assert_called_once_with(var, None)
    mock_create.assert_called_once_with(var, None)
