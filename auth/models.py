
from sqlalchemy import Column, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from db.core import Base
from enums import Roles
from models import TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, default=Roles.user)

    polls = relationship("Poll", back_populates="owner")
    documents = relationship("Document", back_populates="owner")
    notifications = relationship("Notification", back_populates="user")
    posts = relationship("Post", back_populates="owner")
    parcels = relationship("Parcel", back_populates="owner")
    tickets = relationship("Ticket", back_populates="owner")
