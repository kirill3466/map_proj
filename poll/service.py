from typing import Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .models import Option, Poll, Vote
from .schema import PollCreate, PollUpdate


def create(*, db_session: Session, poll: PollCreate, user_id: int) -> Poll:
    options = poll.options
    poll = Poll(question=poll.question,  owner_id=user_id)
    db_session.add(poll)
    db_session.commit()
    db_session.refresh(poll)

    for option in options:
        option = Option(text=option.text, poll_id=poll.id)
        db_session.add(option)
    db_session.commit()
    return poll


def update(
    *,
    db_session: Session,
    poll_id: int,
    poll_update: PollUpdate
) -> Poll:
    poll = get(db_session=db_session, poll_id=poll_id)
    poll.question = poll_update.question

    if poll_update.options:
        for option in poll.options:
            db_session.delete(option)
        for option in poll_update.options:
            new_option = Option(text=option.text, poll_id=poll.id)
            db_session.add(new_option)

    db_session.commit()
    db_session.refresh(poll)
    return poll


def get(*, db_session: Session, poll_id: int) -> Optional[Poll]:
    return db_session.query(Poll).filter(
        Poll.id == poll_id
    ).one_or_none()


def get_all(*, db_session: Session) -> list[Poll]:
    poll = db_session.query(Poll).all()
    return poll


def delete(*, db_session: Session, poll_id: int) -> None:
    poll = db_session.query(Poll).filter(Poll.id == poll_id).first()
    db_session.delete(poll)
    db_session.commit()


def vote(*, db_session: Session, option_id: int) -> Option:
    option = db_session.query(Option).get(option_id)
    option.votes += 1
    db_session.commit()
    db_session.refresh(option)
    return option


def has_user_voted(
    db_session: Session,
    poll_id: int,
    user_identifier: str
) -> bool:
    return db_session.query(Vote).filter(
        Vote.poll_id == poll_id,
        Vote.user_identifier == user_identifier
    ).first() is not None


def cast_vote(
    db_session: Session,
    poll_id: int,
    option_id: int,
    user_identifier: str
):
    existing_vote = db_session.query(Vote).filter(
        Vote.poll_id == poll_id,
        Vote.user_identifier == user_identifier
    ).first()

    if existing_vote:
        raise HTTPException(status_code=400, detail="Вы уже проголосовали")

    option = db_session.query(Option).get(option_id)
    option.votes_count += 1

    vote = Vote(
        poll_id=poll_id,
        option_id=option_id,
        user_identifier=user_identifier
    )
    db_session.add(vote)
    db_session.commit()
    db_session.refresh(option)
    return option
