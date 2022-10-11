import uuid

from pydantic import BaseModel


class UUIDModel(BaseModel):
    id: uuid.UUID
