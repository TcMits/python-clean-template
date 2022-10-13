from contextvars import ContextVar
from typing import Any, Dict, Type, TypeVar

from sqlalchemy.orm import Session

from internal.repository.base import (
    DeleteRepository,
    DeleteWithSessionRepository,
    RepositoryWithEngine,
)
from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class SimpleDeleteRepository(
    DeleteWithSessionRepository[ModelType],
    DeleteRepository[ModelType],
    RepositoryWithEngine,
):
    _model_class: Type[ModelType]

    def delete_with_session(
        self, _: ContextVar[Dict[Any, Any]], session: Session, obj: ModelType
    ) -> None:
        session.delete(obj)

    def delete(self, ctx: ContextVar[Dict[Any, Any]], obj: ModelType) -> None:
        with Session(self._engine) as session:
            self.delete_with_session(ctx, session, obj)
            session.commit()
