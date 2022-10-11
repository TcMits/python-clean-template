from typing import Optional

from pydantic import BaseModel, EmailStr

from pkg.schemas import UUIDModel


class User(BaseModel):
    jwt_token_key: str = ""
    password: Optional[str] = None
    username: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    is_staff: bool = False
    is_superuser: bool = False
    is_active: bool = True


class UserInDB(UUIDModel, User):
    class Config:
        orm_mode = True
