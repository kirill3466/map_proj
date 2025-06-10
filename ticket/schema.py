from pydantic import BaseModel
from enum import Enum
from typing import Optional


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TicketBase(BaseModel):
    title: str
    description: str
    status: Optional[TicketStatus] = TicketStatus.OPEN
    priority: Optional[TicketPriority] = TicketPriority.MEDIUM


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    pass


class TicketRead(TicketBase):
    id: int
    owner_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
