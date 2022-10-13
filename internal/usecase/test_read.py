from contextvars import ContextVar
from typing import Any, Dict
from unittest.mock import MagicMock

from internal.usecase.read import SimpleGetUseCase, SimpleListUseCase

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


def test_simplegetusecase_get():
    mock_get = MagicMock(return_value=1)
    mock_fi_to_fc = MagicMock(return_value=[None])

    class MockGetRepository:
        get = mock_get

    uc = SimpleGetUseCase(MockGetRepository(), mock_fi_to_fc)
    assert uc.get(var, None)
    mock_fi_to_fc.assert_called_once_with(var, None)
    mock_get.assert_called_once_with(var, None)


def test_simplelistusecase_list():
    mock_list = MagicMock(return_value=1)
    mock_fi_to_fc = MagicMock(return_value=[None])
    mock_obi_to_obc = MagicMock(return_value=[None])

    class MockListRepository:
        list = mock_list

    uc = SimpleListUseCase(MockListRepository(), mock_fi_to_fc, mock_obi_to_obc)
    assert uc.list(var, None, None)
    mock_fi_to_fc.assert_called_once_with(var, None)
    mock_obi_to_obc.assert_called_once_with(var, None)
    mock_list.assert_called_once_with(var, [None], [None], offset=0, limit=10)
