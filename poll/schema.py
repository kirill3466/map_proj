from typing import List, Optional
from pydantic import BaseModel


class OptionBase(BaseModel):
    text: str
    id: Optional[int] = None


class OptionCreate(OptionBase):
    pass


class PollBase(BaseModel):
    question: str
    options: Optional[List[OptionBase]] = []


class PollCreate(PollBase):
    pass


class PollUpdate(PollBase):
    question: Optional[str] = None


class PollRead(PollBase):
    id: int


class VoteCreate(BaseModel):
    option_id: int
