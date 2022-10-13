from contextvars import ContextVar
from typing import Any, Dict, Type, TypeVar

from sqlalchemy.orm import Session

from internal.repository.base import (
    RepositoryWithEngine,
    UpdateRepository,
    UpdateWithSessionRepository,
)
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class SimpleUpdateRepository(
    UpdateWithSessionRepository[ModelType],
    UpdateRepository[ModelType],
    RepositoryWithEngine,
):
    _model_class: Type[ModelType]

    def update_with_session(
        self,
        _: ContextVar[Dict[Any, Any]],
        session: Session,
        obj: ModelType,
        obj_in: Dict[str, Any],
    ) -> ModelType:
        for field in obj_in:
            setattr(obj, field, obj_in[field])
        with session.no_autoflush:
            session.add(obj)
            session.flush(objects=[obj])
            if obj.id is None:
                session.refresh(obj)
        return obj

    def update(
        self, ctx: ContextVar[Dict[Any, Any]], obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        with Session(self._engine) as session:
            obj = self.update_with_session(ctx, session, obj, obj_in)
            session.commit()
        return obj
