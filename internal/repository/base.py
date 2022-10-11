from abc import ABC, abstractmethod
from contextvars import ContextVar
from typing import Dict, Generic, Iterable, TypeVar

from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ClauseElement

from pkg.dao.base import DAOBase
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class GetRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def get(self, _: ContextVar[Dict[Any, Any]], *clauses: ClauseElement) -> ModelType:
        pass


class ListRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def list(
        self,
        _: ContextVar[Dict[Any, Any]],
        filter_clauses: Iterable[ClauseElement],
        order_clauses: Iterable[ClauseElement],
        *,
        offset: int = 0,
        limit: int = 10,
    ) -> ModelType:
        pass


class CreateRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def create(
        self, _: ContextVar[Dict[Any, Any]], obj_in: Dict[str, Any]
    ) -> ModelType:
        pass


class UpdateRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def update(
        self, _: ContextVar[Dict[Any, Any]], obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        pass


class DeleteRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def delete(self, _: ContextVar[Dict[Any, Any]], obj: ModelType):
        pass


class SimpleCRUDRepository(
    Generic[ModelType],
    GetRepository[ModelType],
    ListRepository[ModelType],
    CreateRepository[ModelType],
    UpdateRepository[ModelType],
    DeleteRepository[ModelType],
):
    def __init__(self, engine: Engine, dao: DAOBase[ModelType]) -> None:
        self._engine = engine
        self._dao = dao
        super().__init__()

    def get(self, _: ContextVar[Dict[Any, Any]], *clauses: ClauseElement) -> ModelType:
        with Session(self._engine) as session:
            return self._dao.get(session, *clauses)

    def list(
        self,
        _: ContextVar[Dict[Any, Any]],
        filter_clauses: Iterable[ClauseElement],
        order_clauses: Iterable[ClauseElement],
        *,
        offset: int = 0,
        limit: int = 10,
    ) -> ModelType:
        with Session(self._engine) as session:
            return self._dao.get(
                session, filter_clauses, order_clauses, offset=offset, limit=limit
            )

    def create(
        self, _: ContextVar[Dict[Any, Any]], obj_in: Dict[str, Any]
    ) -> ModelType:
        with Session(self._engine) as session:
            return self._dao.create(session, obj_in)

    def update(
        self, _: ContextVar[Dict[Any, Any]], obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        with Session(self._engine) as session:
            return self._dao.update(session, obj, obj_in)

    def delete(self, _: ContextVar[Dict[Any, Any]], obj: ModelType):
        with Session(self._engine) as session:
            return self._dao.delete(session, obj)
