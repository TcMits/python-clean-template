from contextvars import ContextVar
from typing import Any, Dict
from unittest.mock import MagicMock

from internal.usecase.update import SimpleGetAndUpdateUseCase

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


def test_simplegetandupdateusecase_get_and_update():
    mock_get = MagicMock(return_value=2)
    mock_update = MagicMock(return_value=1)
    mock_v = MagicMock(return_value=None)

    class MockGetUseCase:
        get = mock_get

    class MockUpdateRepository:
        update = mock_update

    uc = SimpleGetAndUpdateUseCase(MockUpdateRepository(), MockGetUseCase(), mock_v)
    assert uc.get_and_update(var, None, None)
    mock_get.assert_called_once_with(var, None)
    mock_v.assert_called_once_with(var, 2, None)
    mock_update.assert_called_once_with(var, 2, None)
