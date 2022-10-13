import uuid
from contextvars import ContextVar
from typing import Any, Dict

from internal.repository import test_init
from internal.repository.delete import SimpleDeleteRepository
from pkg.models.base import Base

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


class FakeDeleteModel(Base):
    pass


class FakeDeleteRepository(SimpleDeleteRepository[FakeDeleteModel]):
    _model_class = FakeDeleteModel  # type: ignore


def test_simpledeleterepository_delete(mocker):
    session_mock = mocker.patch("internal.repository.delete.Session")
    fake_query = test_init.Fake()
    session_mock.return_value.__enter__.return_value = fake_query
    repo = FakeDeleteRepository(None)
    obj = FakeDeleteModel()

    assert repo.delete(var, obj) == None
    session_mock.assert_called_once_with(None)
    assert len(fake_query.mock_funcs) == 2
    fake_query.mock_funcs[0].assert_called_with(obj)
    fake_query.mock_funcs[1].assert_called_with()
