from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    code: str
    detail: Any = None


class RefreshTokenResponse(BaseModel):
    token: str
