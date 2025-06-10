from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from auth.auth import CurrUser
from db.core import DbSession
from settings import templates

from .schema import OptionCreate, PollCreate, PollRead, PollUpdate
from .service import (
    cast_vote,
    create,
    delete,
    get,
    get_all,
    has_user_voted,
    update,
)

router = APIRouter()


@router.get("/create", response_class=HTMLResponse)
def create_poll_form(
    request: Request,
    current_user: CurrUser
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не авторизованы"
        )
    return templates.TemplateResponse(
        "partials/poll_create.html",
        {"request": request, "poll": None, "current_user": current_user}
    )


@router.get("/{poll_id}/edit", response_class=HTMLResponse)
def edit_poll_form(
    request: Request,
    db_session: DbSession,
    poll_id: int,
    current_user: CurrUser
):
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll or poll.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return templates.TemplateResponse(
        "partials/poll_form.html",
        {"request": request, "poll": poll, "current_user": current_user}
    )


@router.get("/{poll_id}", response_class=HTMLResponse)
def get_poll_page(
    request: Request,
    db_session: DbSession,
    poll_id: int,
    current_user: CurrUser
):
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Голосование не найдено")

    user_identifier = request.client.host
    already_voted = has_user_voted(db_session, poll_id, user_identifier)

    return templates.TemplateResponse(
        "partials/poll.html",
        {
            "request": request,
            "poll": poll,
            "current_user": current_user,
            "already_voted": already_voted
        }
    )


@router.get("", response_class=HTMLResponse)
def get_all_polls(
    request: Request,
    db_session: DbSession,
    current_user: CurrUser
):
    polls = get_all(db_session=db_session)
    return templates.TemplateResponse(
        "partials/polls.html",
        {"request": request, "polls": polls, "current_user": current_user}
    )


@router.post("/create", response_class=RedirectResponse)
async def submit_poll_form(
    db_session: DbSession,
    current_user: CurrUser,
    request: Request
):
    form_data = await request.form()

    question = form_data.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Вопрос обязателен")

    options = []
    for key in form_data:
        if key.startswith("option_"):
            value = form_data[key]
            if value:
                options.append(OptionCreate(text=value))

    if len(options) < 2:
        raise HTTPException(
            status_code=400, detail="Минимум 2 варианта ответа"
        )

    poll_in = PollCreate(question=question, options=options)
    create(db_session=db_session, poll=poll_in, user_id=current_user.id)
    return RedirectResponse("/polls", status_code=303)


@router.post("/{poll_id}/edit", response_class=RedirectResponse)
async def submit_poll_edit_form(
    db_session: DbSession,
    poll_id: int,
    current_user: CurrUser,
    request: Request
):
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll or poll.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    form_data = await request.form()
    question = form_data.get("question")
    options = []

    for key in form_data:
        if key.startswith("option_"):
            value = form_data[key]
            if value:
                options.append(OptionCreate(text=value))

    if len(options) < 2:
        raise HTTPException(
            status_code=400, detail="Минимум 2 варианта ответа"
        )

    poll_in = PollUpdate(question=question, options=options)
    update(db_session=db_session, poll_id=poll_id, poll_update=poll_in)
    return RedirectResponse("/polls", status_code=303)


@router.post("/{poll_id}/delete", response_class=HTMLResponse)
def delete_poll(
    request: Request,
    db_session: DbSession,
    poll_id: int,
    current_user: CurrUser
):
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll or poll.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    delete(db_session=db_session, poll_id=poll_id)
    return RedirectResponse("/polls", status_code=303)


@router.get("/{poll_id:int}", response_model=PollRead)
def get_poll_api(db_session: DbSession, poll_id: int):
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Голосование не найдено"
        )
    return poll


@router.post("", response_model=PollRead)
def create_poll_api(
    db_session: DbSession,
    poll_in: PollCreate,
    current_user: CurrUser
):
    return create(db_session=db_session, poll=poll_in, user_id=current_user.id)


@router.put("/{poll_id}", response_model=PollRead)
def update_poll_api(
    db_session: DbSession,
    poll_id: int,
    poll_in: PollUpdate,
    current_user: CurrUser
):
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Голосование не найдено"
        )
    return update(db_session=db_session, poll_id=poll_id, poll_update=poll_in)


@router.post("/vote", response_class=RedirectResponse)
def cast_vote_route(
    request: Request,
    db_session: DbSession,
    poll_id: int = Form(...),
    option_id: int = Form(...)
):
    user_identifier = request.client.host
    cast_vote(db_session, poll_id, option_id, user_identifier)
    return RedirectResponse(f"/polls/{poll_id}", status_code=303)
