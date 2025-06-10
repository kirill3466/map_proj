from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from auth.auth import CurrUser
from db.core import DbSession
from settings import templates

from .models import TicketPriority, TicketStatus
from .schema import TicketCreate, TicketUpdate
from .service import create, delete, get_all, get_by_id, update

router = APIRouter()


@router.get("", response_class=HTMLResponse)
def get_all_tickets(
    request: Request,
    db_session: DbSession,
    current_user: CurrUser
):
    tickets = get_all(db_session=db_session)
    return templates.TemplateResponse(
        "partials/tickets.html",
        {"request": request, "tickets": tickets, "current_user": current_user}
    )


@router.get("/create", response_class=HTMLResponse)
def create_ticket_form(
    request: Request,
    current_user: CurrUser
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return templates.TemplateResponse(
        "partials/ticket_create.html",
        {"request": request, "ticket": None, "current_user": current_user}
    )


@router.post("/create", response_class=RedirectResponse)
async def submit_ticket_form(
    db_session: DbSession,
    current_user: CurrUser,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form("medium")
):
    try:
        ticket_in = TicketCreate(
            title=title,
            description=description,
            priority=TicketPriority(priority.lower()),
        )
        create(db_session=db_session, ticket_in=ticket_in, user_id=current_user.id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверное значение приоритета")

    return RedirectResponse("/tickets", status_code=303)


@router.get("/{ticket_id}", response_class=HTMLResponse)
def view_ticket(
    request: Request,
    db_session: DbSession,
    ticket_id: int,
    current_user: CurrUser
):
    ticket = get_by_id(db_session=db_session, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return templates.TemplateResponse(
        "partials/ticket.html",
        {"request": request, "ticket": ticket, "current_user": current_user}
    )


@router.get("/{ticket_id}/edit", response_class=HTMLResponse)
def edit_ticket_form(
    request: Request,
    db_session: DbSession,
    ticket_id: int,
    current_user: CurrUser
):
    ticket = get_by_id(db_session=db_session, ticket_id=ticket_id)
    if not ticket or ticket.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return templates.TemplateResponse(
        "partials/ticket_create.html",
        {"request": request, "ticket": ticket, "current_user": current_user}
    )


@router.post("/{ticket_id}/edit", response_class=RedirectResponse)
async def submit_ticket_edit_form(
    db_session: DbSession,
    ticket_id: int,
    current_user: CurrUser,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    status: str = Form(...)
):
    try:
        ticket = get_by_id(db_session=db_session, ticket_id=ticket_id)
        if not ticket or ticket.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        ticket_in = TicketUpdate(
            title=title,
            description=description,
            priority=TicketPriority(priority.lower()).value,
            status=TicketStatus(status.lower()).value
        )

        update(db_session=db_session, ticket_id=ticket_id, ticket_in=ticket_in)

    except ValueError:
        raise HTTPException(status_code=400, detail="Неверное значение статуса или приоритета")

    return RedirectResponse(f"/tickets/{ticket_id}", status_code=303)


@router.post("/{ticket_id}/delete", response_class=HTMLResponse)
def delete_ticket(
    db_session: DbSession,
    ticket_id: int,
    current_user: CurrUser
):
    ticket = get_by_id(db_session=db_session, ticket_id=ticket_id)
    if not ticket or ticket.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    delete(db_session=db_session, ticket_id=ticket_id)
    return RedirectResponse("/tickets", status_code=303)
