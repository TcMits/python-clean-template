from contextvars import ContextVar
from typing import Any, Callable, Dict, TypeVar

from internal.repository.base import UpdateRepository
from internal.usecase.base import GetAndUpdateUseCase, GetUseCase
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
FilterInputType = TypeVar("FilterInputType")
UpdateInputType = TypeVar("UpdateInputType")


class SimpleGetAndUpdateUseCase(
    GetAndUpdateUseCase[ModelType, FilterInputType, UpdateInputType]
):
    def __init__(
        self,
        update_repository: UpdateRepository[ModelType],
        get_use_case: GetUseCase[ModelType, FilterInputType],
        validate_func: Callable[
            [ContextVar[Dict[Any, Any]], ModelType, UpdateInputType], Dict[str, Any]
        ],
    ) -> None:
        self._update_repository = update_repository
        self._get_use_case = get_use_case
        self._validate_func = validate_func
        super().__init__()

    def get_and_update(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        filter_input: FilterInputType,
        update_input: UpdateInputType,
    ) -> ModelType:
        obj = self._get_use_case.get(ctx, filter_input)
        validated_data = self._validate_func(ctx, obj, update_input)
        return self._update_repository.update(ctx, obj, validated_data)
