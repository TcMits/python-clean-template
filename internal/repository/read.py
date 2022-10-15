from contextvars import ContextVar
from typing import Any, Dict, Iterable, List, Type, TypeVar

from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ClauseElement

from internal.repository.base import (
    GetRepository,
    GetWithSessionRepository,
    ListRepository,
    ListWithSessionRepository,
    RepositoryWithEngine,
)
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class SimpleGetRepository(
    GetWithSessionRepository[ModelType],
    GetRepository[ModelType],
    RepositoryWithEngine,
):
    _model_class: Type[ModelType]

    def get_with_session(
        self,
        _: ContextVar[Dict[Any, Any]],
        session: Session,
        *clauses: ClauseElement,
        with_for_update: bool = False,
    ) -> ModelType:
        query = session.query(self._model_class).filter(*clauses)
        if with_for_update:
            query = query.with_for_update()
        return query.one()

    def get(
        self, ctx: ContextVar[Dict[Any, Any]], *clauses: ClauseElement
    ) -> ModelType:
        with Session(self._engine) as session:
            return self.get_with_session(ctx, session, *clauses)


class SimpleListRepository(
    ListWithSessionRepository[ModelType],
    ListRepository[ModelType],
    RepositoryWithEngine,
):
    _model_class: Type[ModelType]

    def list_with_session(
        self,
        _: ContextVar[Dict[Any, Any]],
        session: Session,
        filter_clauses: Iterable[ClauseElement],
        order_by_clauses: Iterable[ClauseElement],
        *,
        offset: int = 0,
        limit: int = 10,
        with_for_update: bool = False,
    ) -> List[ModelType]:
        query = (
            session.query(self._model_class)
            .filter(*filter_clauses)
            .order_by(*order_by_clauses)
            .offset(offset)
            .limit(limit)
        )
        if with_for_update:
            query = query.with_for_update()
        return query.all()

    def list(
        self,
        ctx: ContextVar[Dict[Any, Any]],
        filter_clauses: Iterable[ClauseElement],
        order_by_clauses: Iterable[ClauseElement],
        *,
        offset: int = 0,
        limit: int = 10,
    ) -> List[ModelType]:
        with Session(self._engine) as session:
            return self.list_with_session(
                ctx,
                session,
                filter_clauses,
                order_by_clauses,
                offset=offset,
                limit=limit,
            )
