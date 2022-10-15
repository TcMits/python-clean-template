from pydantic import BaseModel, Field, validator


class LoginInput(BaseModel):
    username: str = Field(min_length=4, max_length=128)
    password: str = Field(min_length=8, max_length=128)

    @validator("username")
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("pkg.schemas.login: username is not alnum")
        return v


class RefreshTokenInput(BaseModel):
    refresh_token: str = Field(min_length=1)
    refresh_key: str = Field(min_length=1)


class JWTAuthenticatedPayload(BaseModel):
    access_token: str = Field(min_length=1)
    refresh_token: str = Field(min_length=1)
    refresh_key: str = Field(min_length=1)
