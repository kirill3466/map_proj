from sqlalchemy.orm import Session
from .models import Ticket
from .schema import TicketCreate, TicketUpdate


def create(
    *,
    db_session: Session,
    ticket_in: TicketCreate,
    user_id: int
) -> Ticket:
    ticket = Ticket(**ticket_in.model_dump(), owner_id=user_id)
    db_session.add(ticket)
    db_session.commit()
    db_session.refresh(ticket)
    return ticket


def get_all(*, db_session: Session) -> list[Ticket]:
    return db_session.query(Ticket).all()


def get_by_id(*, db_session: Session, ticket_id: int) -> Ticket:
    return db_session.query(Ticket).filter(Ticket.id == ticket_id).first()


def update(
    *,
    db_session: Session,
    ticket_id: int,
    ticket_in: TicketUpdate
) -> Ticket:
    ticket = get_by_id(db_session=db_session, ticket_id=ticket_id)
    if not ticket:
        raise Exception("Ticket not found")
    for key, value in ticket_in.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)
    db_session.commit()
    db_session.refresh(ticket)
    return ticket


def delete(*, db_session: Session, ticket_id: int):
    ticket = get_by_id(db_session=db_session, ticket_id=ticket_id)
    db_session.delete(ticket)
    db_session.commit()
