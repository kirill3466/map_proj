from typing import Optional

from models import Base


class PostRead(Base):
    id: Optional[int]
    owner_id: int
    title: str
    content: str


class PostCreate(Base):
    title: str
    content: str


class PostUpdate(Base):
    title: Optional[str]
    content: Optional[str]
