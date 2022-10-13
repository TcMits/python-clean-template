from contextvars import ContextVar
from typing import Any, Dict, TypeVar

from internal.repository.base import DeleteRepository
from internal.usecase.base import GetAndDeleteUseCase, GetUseCase
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
FilterInputType = TypeVar("FilterInputType")


class SimpleGetAndDeleteUseCase(GetAndDeleteUseCase[ModelType, FilterInputType]):
    def __init__(
        self,
        delete_repository: DeleteRepository[ModelType],
        get_use_case: GetUseCase[ModelType, FilterInputType],
    ) -> None:
        self._delete_repository = delete_repository
        self._get_use_case = get_use_case
        super().__init__()

    def get_and_delete(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        filter_input: FilterInputType,
    ) -> None:
        obj = self._get_use_case.get(ctx, filter_input)
        self._delete_repository.delete(ctx, obj)
