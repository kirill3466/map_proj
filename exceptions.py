from typing import ClassVar

from pydantic import BaseModel


class InvalidConfigError(BaseModel):
    code: ClassVar[str] = "invalid.config"
    msg_template: str = "{msg}"


class InvalidUsernamePasswordError(BaseModel):
    code: ClassVar[str] = "invalid.username.password"
    msg_template: str = "{msg}"


class NotAuthenticatedException(Exception):
    pass
