from abc import ABC, abstractmethod
from contextvars import ContextVar
from typing import Dict, Generic, Iterable, List, TypeVar

from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ClauseElement

from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class GetWithSessionRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def get_with_session(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        session: Session,
        *clauses: ClauseElement,
        with_for_update: bool = False,
    ) -> ModelType:
        pass


class GetRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def get(
        self, ctx: ContextVar[Dict[Any, Any]], *clauses: ClauseElement
    ) -> ModelType:
        pass


class ListWithSessionRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def list_with_session(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        session: Session,
        filter_clauses: Iterable[ClauseElement],
        order_clauses: Iterable[ClauseElement],
        *,
        offset: int = 0,
        limit: int = 10,
        with_for_update: bool = False,
    ) -> List[ModelType]:
        pass


class ListRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def list(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        filter_clauses: Iterable[ClauseElement],
        order_clauses: Iterable[ClauseElement],
        *,
        offset: int = 0,
        limit: int = 10,
    ) -> List[ModelType]:
        pass


class CreateWithSessionRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def create_with_session(
        self, ctx: ContextVar[Dict[Any, Any]], session: Session, obj_in: Dict[str, Any]
    ) -> ModelType:
        pass


class CreateRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def create(
        self, ctx: ContextVar[Dict[Any, Any]], obj_in: Dict[str, Any]
    ) -> ModelType:
        pass


class UpdateWithSessionRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def update_with_session(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        session: Session,
        obj: ModelType,
        obj_in: Dict[str, Any],
    ) -> ModelType:
        pass


class UpdateRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def update(
        self, ctx: ContextVar[Dict[Any, Any]], obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        pass


class DeleteWithSessionRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def delete_with_session(
        self, ctx: ContextVar[Dict[Any, Any]], session: Session, obj: ModelType
    ) -> None:
        pass


class DeleteRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def delete(self, ctx: ContextVar[Dict[Any, Any]], obj: ModelType) -> None:
        pass


class RepositoryWithEngine:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        super().__init__()
