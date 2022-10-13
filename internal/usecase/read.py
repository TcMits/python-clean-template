from contextvars import ContextVar
from typing import Any, Callable, Dict, Iterable, TypeVar

from sqlalchemy.sql.elements import ClauseElement

from internal.repository.base import GetRepository, ListRepository
from internal.usecase.base import GetUseCase, ListUseCase
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
FilterInputType = TypeVar("FilterInputType")
OrderByInputType = TypeVar("OrderByInputType")


class SimpleGetUseCase(GetUseCase[ModelType, FilterInputType]):
    def __init__(
        self,
        get_repository: GetRepository[ModelType],
        filter_input_to_filter_clauses_func: Callable[
            [ContextVar[Dict[Any, Any]], FilterInputType], Iterable[ClauseElement]
        ],
    ) -> None:
        self._get_repository = get_repository
        self._filter_input_to_filter_clauses_func = filter_input_to_filter_clauses_func
        super().__init__()

    def get(
        self, ctx: ContextVar[Dict[Any, Any]], filter_input: FilterInputType
    ) -> ModelType:
        filter_clauses = self._filter_input_to_filter_clauses_func(ctx, filter_input)
        return self._get_repository.get(ctx, *filter_clauses)


class SimpleListUseCase(ListUseCase[ModelType, FilterInputType, OrderByInputType]):
    def __init__(
        self,
        list_repository: ListRepository[ModelType],
        filter_input_to_filter_clauses_func: Callable[
            [ContextVar[Dict[Any, Any]], FilterInputType], Iterable[ClauseElement]
        ],
        order_by_input_to_order_by_clauses_func: Callable[
            [ContextVar[Dict[Any, Any]], OrderByInputType], Iterable[ClauseElement]
        ],
    ) -> None:
        self._list_repository = list_repository
        self._filter_input_to_filter_clauses_func = filter_input_to_filter_clauses_func
        self._order_by_input_to_order_by_clauses_func = (
            order_by_input_to_order_by_clauses_func
        )
        super().__init__()

    def list(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        filter_input: FilterInputType,
        order_by_input: OrderByInputType,
        *,
        offset: int = 0,
        limit: int = 10
    ) -> ModelType:
        filter_clauses = self._filter_input_to_filter_clauses_func(ctx, filter_input)
        order_by_clauses = self._order_by_input_to_order_by_clauses_func(
            ctx, order_by_input
        )
        return self._list_repository.list(
            ctx, filter_clauses, order_by_clauses, offset=offset, limit=limit
        )
