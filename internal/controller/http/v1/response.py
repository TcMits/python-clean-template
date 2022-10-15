from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    code: str


class RefreshTokenResponse(BaseModel):
    token: str
