from contextvars import ContextVar
from typing import Any, Dict
from unittest.mock import MagicMock

from internal.usecase.delete import SimpleGetAndDeleteUseCase

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


def test_simplegetanddeleteusecase_get_and_delete():
    mock_get = MagicMock(return_value=2)
    mock_delete = MagicMock(return_value=1)

    class MockGetUseCase:
        get = mock_get

    class MockDeleteRepository:
        delete = mock_delete

    uc = SimpleGetAndDeleteUseCase(MockDeleteRepository(), MockGetUseCase())
    assert uc.get_and_delete(var, None) == None
    mock_get.assert_called_once_with(var, None)
    mock_delete.assert_called_once_with(var, 2)
