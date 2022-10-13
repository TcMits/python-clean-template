from contextvars import ContextVar
from typing import Any, Dict, Type, TypeVar

from sqlalchemy.orm import Session

from internal.repository.base import (
    CreateRepository,
    CreateWithSessionRepository,
    RepositoryWithEngine,
)
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class SimpleCreateRepository(
    CreateWithSessionRepository[ModelType],
    CreateRepository[ModelType],
    RepositoryWithEngine,
):
    _model_class: Type[ModelType]

    def create_with_session(
        self, _: ContextVar[Dict[Any, Any]], session: Session, obj_in: Dict[str, Any]
    ) -> ModelType:
        obj = self._model_class(**obj_in)  # type: ignore
        with session.no_autoflush:
            session.add(obj)
            session.flush(objects=[obj])
            if obj.id is None:
                session.refresh(obj)
        return obj

    def create(
        self, ctx: ContextVar[Dict[Any, Any]], obj_in: Dict[str, Any]
    ) -> ModelType:
        with Session(self._engine) as session:
            obj = self.create_with_session(ctx, session, obj_in)
            session.commit()
        return obj
