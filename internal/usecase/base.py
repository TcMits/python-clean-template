from abc import ABC, abstractmethod
from contextvars import ContextVar
from typing import Any, Dict, Generic, List, TypeVar

from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
FilterInputType = TypeVar("FilterInputType")
OrderByInputType = TypeVar("OrderByInputType")
CreateInputType = TypeVar("CreateInputType")
UpdateInputType = TypeVar("UpdateInputType")
LoginInputType = TypeVar("LoginInputType")
AuthenticatedPayloadType = TypeVar("AuthenticatedPayloadType")
RefreshTokenInputType = TypeVar("RefreshTokenInputType")


class GetUseCase(ABC, Generic[ModelType, FilterInputType]):
    @abstractmethod
    def get(
        self, ctx: ContextVar[Dict[Any, Any]], filter_input: FilterInputType
    ) -> ModelType:
        pass


class ListUseCase(ABC, Generic[ModelType, FilterInputType, OrderByInputType]):
    @abstractmethod
    def list(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        filter_input: FilterInputType,
        order_by_input: OrderByInputType,
        *,
        offset: int = 0,
        limit: int = 10,
    ) -> List[ModelType]:
        pass


class CreateUseCase(ABC, Generic[ModelType, CreateInputType]):
    @abstractmethod
    def create(
        self, ctx: ContextVar[Dict[Any, Any]], create_input: CreateInputType
    ) -> ModelType:
        pass


class GetAndUpdateUseCase(ABC, Generic[ModelType, FilterInputType, UpdateInputType]):
    @abstractmethod
    def get_and_update(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        filter_input: FilterInputType,
        update_input: UpdateInputType,
    ) -> ModelType:
        pass


class GetAndDeleteUseCase(ABC, Generic[ModelType, FilterInputType]):
    @abstractmethod
    def get_and_delete(
        self, ctx: ContextVar[Dict[Any, Any]], filter_input: FilterInputType
    ) -> None:
        pass


class LoginUseCase(
    ABC,
    Generic[ModelType, LoginInputType, AuthenticatedPayloadType, RefreshTokenInputType],
):
    @abstractmethod
    def login(
        self, ctx: ContextVar[Dict[Any, Any]], login_input: LoginInputType
    ) -> AuthenticatedPayloadType:
        pass

    @abstractmethod
    def verify_token(self, ctx: ContextVar[Dict[Any, Any]], token: str) -> ModelType:
        pass

    @abstractmethod
    def refresh_token(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        refresh_token_input: RefreshTokenInputType,
    ) -> str:
        pass
