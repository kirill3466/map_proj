from models import Base


class DocumentCreate(Base):
    filename: str


class Document(Base):
    filename: str
    user_id: int


class DocumentRead(Base):
    id: int
    user_id: int
    filename: str


class DocumentUpdate(Base):
    filename: str
