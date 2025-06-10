from models import Base


class NotificationCreate(Base):
    user_id: int
    message: str


class NotificationUpdate(Base):
    message: str


class NotificationRead(Base):
    id: int
    user_id: int
    message: str
