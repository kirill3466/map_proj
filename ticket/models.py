from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from db.core import Base
from enum import StrEnum


class TicketStatus(StrEnum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class TicketPriority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    status = Column(SqlEnum(TicketStatus), default=TicketStatus.open)
    priority = Column(SqlEnum(TicketPriority), default=TicketPriority.medium)
    created_at = Column(DateTime, server_default="now()")
    updated_at = Column(
        DateTime, server_default="now()", server_onupdate="now()"
    )

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tickets")
