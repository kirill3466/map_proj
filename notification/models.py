from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.core import Base
from models import TimeStampMixin


class Notification(Base, TimeStampMixin):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")
