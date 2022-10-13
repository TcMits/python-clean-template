import uuid
from contextvars import ContextVar
from typing import Any, Dict

from internal.repository import test_init
from internal.repository.update import SimpleUpdateRepository
from pkg.models.base import Base

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


class FakeUpdateModel(Base):
    pass


class FakeSimpleCRUDRepository(SimpleUpdateRepository[FakeUpdateModel]):
    _model_class = FakeUpdateModel  # type: ignore


def test_simpleupdaterepository_update(mocker):
    session_mock = mocker.patch("internal.repository.update.Session")
    fake_query = test_init.Fake()
    session_mock.return_value.__enter__.return_value = fake_query
    repo = FakeSimpleCRUDRepository(None)
    obj_in = {}
    obj = FakeUpdateModel()

    assert repo.update(var, obj, obj_in) == obj
    session_mock.assert_called_once_with(None)
    assert len(fake_query.mock_funcs) == 5
    fake_query.mock_funcs[0].assert_called_with()
    fake_query.mock_funcs[1].assert_called_with(obj)
    fake_query.mock_funcs[2].assert_called_with(objects=[obj])
    fake_query.mock_funcs[3].assert_called_with(obj)
    fake_query.mock_funcs[4].assert_called_with()
