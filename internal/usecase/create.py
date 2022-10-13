from contextvars import ContextVar
from typing import Any, Callable, Dict, TypeVar

from internal.repository.base import CreateRepository
from internal.usecase.base import CreateUseCase
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateInputType = TypeVar("CreateInputType")


class SimpleCreateUseCase(CreateUseCase[ModelType, CreateInputType]):
    def __init__(
        self,
        create_repository: CreateRepository[ModelType],
        validate_func: Callable[
            [ContextVar[Dict[Any, Any]], CreateInputType], Dict[str, Any]
        ],
    ) -> None:
        self._create_repository = create_repository
        self._validate_func = validate_func
        super().__init__()

    def create(
        self, ctx: ContextVar[Dict[Any, Any]], create_input: CreateInputType
    ) -> ModelType:
        validated_data = self._validate_func(ctx, create_input)
        return self._create_repository.create(ctx, validated_data)
