from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ClauseElement

from pkg.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class DAOBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        DAO (database access object) with default methods to Create, Read, Update, Delete,...
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, *clauses: ClauseElement) -> Optional[ModelType]:
        return db.query(self.model).filter(*clauses).first()

    def get_multi(
        self,
        db: Session,
        filter_clauses: Iterable[ClauseElement],
        order_by_clauses: Iterable[ClauseElement],
        *,
        offset: int = 0,
        limit: int = 10
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter(*filter_clauses)
            .order_by(*order_by_clauses)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def count(self, db: Session, *clauses: ClauseElement) -> int:
        return db.query(self.model).filter(*clauses).count()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        for field in obj_in:
            setattr(obj, field, obj_in[field])
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, obj: ModelType) -> ModelType:
        db.delete(obj)
        db.commit()
        return obj
