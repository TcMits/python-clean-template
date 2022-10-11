from sqlalchemy import Boolean, Column, String

from pkg.models.base import Base


class User(Base):
    jwt_token_key = Column(String(), nullable=False, default="")
    password = Column(String(), nullable=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    first_name = Column(String(128), nullable=False, default="")
    last_name = Column(String(128), nullable=False, default="")
    is_staff = Column(Boolean(), nullable=False, default=False)
    is_superuser = Column(Boolean(), nullable=False, default=False)
    is_active = Column(Boolean(), nullable=False, default=True)
