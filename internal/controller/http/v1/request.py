from pydantic import BaseModel, Field


class VerifyTokenRequest(BaseModel):
    token: str = Field(min_length=1)
