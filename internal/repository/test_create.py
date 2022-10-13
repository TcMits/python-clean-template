import uuid
from contextvars import ContextVar
from typing import Any, Dict

from internal.repository import test_init
from internal.repository.create import SimpleCreateRepository
from pkg.models.base import Base

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


class FakeCreateModel(Base):
    pass


class FakeCreateRepository(SimpleCreateRepository[FakeCreateModel]):
    _model_class = FakeCreateModel  # type: ignore


def test_simplecreaterepository_create(mocker):
    session_mock = mocker.patch("internal.repository.create.Session")
    fake_query = test_init.Fake()
    session_mock.return_value.__enter__.return_value = fake_query
    repo = FakeCreateRepository(None)
    obj_in = {}
    obj = FakeCreateModel()

    def fake_model_class(*args, **kwargs):
        return obj

    repo._model_class = fake_model_class

    assert repo.create(var, obj_in) == obj
    session_mock.assert_called_once_with(None)
    assert len(fake_query.mock_funcs) == 5
    fake_query.mock_funcs[0].assert_called_with()
    fake_query.mock_funcs[1].assert_called_with(obj)
    fake_query.mock_funcs[2].assert_called_with(objects=[obj])
    fake_query.mock_funcs[3].assert_called_with(obj)
    fake_query.mock_funcs[4].assert_called_with()
