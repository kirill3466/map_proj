from typing import Optional

from pydantic import field_validator
from pydantic.fields import Field

from enums import Roles
from models import Base

from .security import generate_password, hash_password


class UserBase(Base):
    email: str

    @field_validator("email")
    def email_required(cls, v):
        if not v:
            raise ValueError("Email должен быть заполнен")
        return v


class UserLogin(UserBase):
    password: str

    @field_validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Пароль должен быть заполнен")
        return v


class UserCreate(UserBase):
    email: str
    password: Optional[str] = Field(None, nullable=True)
    role: Optional[Roles] = Field(default=Roles.user, nullable=True)

    @field_validator("password", mode="before")
    def hash(cls, v):
        return hash_password(str(v))


class UserRegister(UserLogin):
    password: Optional[str] = Field(default=None, nullable=True)

    @field_validator("password")
    def password_required(cls, v):
        password = v or generate_password()
        return hash_password(password)


class UserUpdate(Base):
    first_name: Optional[str] = Field(None, nullable=True)
    last_name: Optional[str] = Field(None, nullable=True)
    password: Optional[str] = Field(None, nullable=True)
    # remove changable role from update endpoint
    # role: Optional[Roles] = Field(None, nullable=True)

    @field_validator("password")
    def hash(cls, v):
        return hash_password(str(v))


class UserRead(UserBase):
    id: int
    role: Optional[Roles] = Field(None, nullable=True)


class UserLoginResponse(Base):
    token: Optional[str] = Field(None, nullable=True)


class Token(Base):
    access_token: str
    token_type: str


class TokenData(Base):
    email: str | None = None
