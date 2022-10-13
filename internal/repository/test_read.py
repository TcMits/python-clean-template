from contextvars import ContextVar
from typing import Any, Dict

from internal.repository import test_init
from internal.repository.read import SimpleGetRepository, SimpleListRepository
from pkg.models.base import Base

var: ContextVar[Dict[Any, Any]] = ContextVar("var", default={})


class FakeReadModel(Base):
    pass


class FakeReadRepository(
    SimpleGetRepository[FakeReadModel],
    SimpleListRepository[FakeReadModel],
):
    _model_class = FakeReadModel  # type: ignore


def test_simplegetrepository_get(mocker):
    session_mock = mocker.patch("internal.repository.read.Session")
    fake_query = test_init.Fake()
    session_mock.return_value.__enter__.return_value = fake_query
    repo = FakeReadRepository(None)
    clause = FakeReadModel.id == "test"

    assert repo.get(var, clause) == fake_query
    session_mock.assert_called_once_with(None)
    assert len(fake_query.mock_funcs) == 3
    fake_query.mock_funcs[0].assert_called_with(FakeReadModel)
    fake_query.mock_funcs[1].assert_called_with(clause)
    fake_query.mock_funcs[2].assert_called_with()


def test_simplegetrepository_get_with_session():
    fake_query = test_init.Fake()
    repo = FakeReadRepository(None)
    clause = FakeReadModel.id == "test"

    assert (
        repo.get_with_session(var, fake_query, clause, with_for_update=True)
        == fake_query
    )
    assert len(fake_query.mock_funcs) == 4
    fake_query.mock_funcs[0].assert_called_with(FakeReadModel)
    fake_query.mock_funcs[1].assert_called_with(clause)
    fake_query.mock_funcs[2].assert_called_with()
    fake_query.mock_funcs[3].assert_called_with()


def test_simplelistrepository_list(mocker):
    session_mock = mocker.patch("internal.repository.read.Session")
    fake_query = test_init.Fake()
    session_mock.return_value.__enter__.return_value = fake_query
    repo = FakeReadRepository(None)
    filter_clauses = [FakeReadModel.id == "test"]
    order_by_clauses = [FakeReadModel.id]

    assert (
        repo.list(var, filter_clauses, order_by_clauses, offset=0, limit=1)
        == fake_query
    )
    session_mock.assert_called_once_with(None)
    assert len(fake_query.mock_funcs) == 6
    fake_query.mock_funcs[0].assert_called_with(FakeReadModel)
    fake_query.mock_funcs[1].assert_called_with(*filter_clauses)
    fake_query.mock_funcs[2].assert_called_with(*order_by_clauses)
    fake_query.mock_funcs[3].assert_called_with(0)
    fake_query.mock_funcs[4].assert_called_with(1)
    fake_query.mock_funcs[5].assert_called_with()


def test_simplelistrepository_list_with_session():
    fake_query = test_init.Fake()
    repo = FakeReadRepository(None)
    filter_clauses = [FakeReadModel.id == "test"]
    order_by_clauses = [FakeReadModel.id]

    assert (
        repo.list_with_session(
            var,
            fake_query,
            filter_clauses,
            order_by_clauses,
            offset=0,
            limit=1,
            with_for_update=True,
        )
        == fake_query
    )
    assert len(fake_query.mock_funcs) == 7
    fake_query.mock_funcs[0].assert_called_with(FakeReadModel)
    fake_query.mock_funcs[1].assert_called_with(*filter_clauses)
    fake_query.mock_funcs[2].assert_called_with(*order_by_clauses)
    fake_query.mock_funcs[3].assert_called_with(0)
    fake_query.mock_funcs[4].assert_called_with(1)
    fake_query.mock_funcs[5].assert_called_with()
    fake_query.mock_funcs[6].assert_called_with()
