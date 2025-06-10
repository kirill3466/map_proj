from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.core import Base


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="polls")
    options = relationship(
        "Option",
        back_populates="poll",
        cascade="all, delete-orphan"
    )


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))

    poll = relationship("Poll", back_populates="options")
    votes = relationship(
        "Vote",
        back_populates="option",
        cascade="all, delete-orphan"
    )
    votes_count = Column(Integer, default=0)


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    user_identifier = Column(String, index=True)

    option = relationship("Option", back_populates="votes")
