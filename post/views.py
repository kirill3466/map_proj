# views.py
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from auth.auth import CurrUser
from db.core import DbSession
from settings import templates
from fastapi import Form

from .schema import PostCreate, PostRead, PostUpdate
from .service import create, delete, get, get_all, get_all_from_user, update

router = APIRouter()


@router.get("/{post_id:int}", response_model=PostRead)
def get_post(db_session: DbSession, post_id: int):
    post = get(
        db_session=db_session,
        post_id=post_id
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден."
        )
    return post


# добавить пагинацию и фильтрацию по времени убрать юзлес секунды в datetime
@router.get("", response_class=HTMLResponse)
def get_all_posts(
    request: Request,
    db_session: DbSession,
    current_user: CurrUser
):
    posts = get_all(db_session=db_session)
    # if not posts:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Посты не найдены."
    #     )
    return templates.TemplateResponse(
        "partials/posts.html",
        {
            "request": request,
            "posts": posts,
            "current_user": current_user
        }
    )


@router.get("/user/{user_id}", response_model=list[PostRead])
def get_user_posts(
    db_session: DbSession,
    user_id: int,
    current_user: CurrUser
):
    posts = get_all_from_user(db_session=db_session, user_id=user_id)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Посты не найдены."
        )
    return posts


@router.post("", response_model=PostRead)
def create_post(
    db_session: DbSession,
    post_in: PostCreate,
    current_user: CurrUser
):
    return create(
        db_session=db_session,
        post_in=post_in,
        user_id=current_user.id
    )


@router.put("/{post_id}", response_model=PostRead)
def update_post(
    db_session: DbSession,
    post_id: int,
    post_in: PostUpdate,
    current_user: CurrUser
):
    post = get(
        db_session=db_session,
        post_id=post_id
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден."
        )
    return update(
        db_session=db_session,
        post=post,
        post_in=post_in
    )


@router.post("/{post_id}/delete", response_class=HTMLResponse)
def delete_post(
    request: Request,
    post_id: int,
    db: DbSession,
    current_user: CurrUser
):
    post = get(db_session=db, post_id=post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    delete(db_session=db, post_id=post_id)
    return RedirectResponse("/posts", status_code=303)


@router.get("/{post_id}/edit", response_class=HTMLResponse)
def edit_post_form(
    request: Request,
    post_id: int,
    db_session: DbSession,
    current_user: CurrUser
):
    post = get(db_session=db_session, post_id=post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return templates.TemplateResponse(
        "partials/post.html",
        {"request": request, "post": post}
    )


@router.post("/{post_id}/edit", response_class=RedirectResponse)
def edit_post_submit(
    request: Request,
    db_session: DbSession,
    current_user: CurrUser,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...)
):
    post = get(db_session=db_session, post_id=post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    post_in = PostUpdate(title=title, content=content)
    update(db_session=db_session, post=post, post_in=post_in)
    return templates.TemplateResponse(
        "partials/post.html",
        {"request": request, "post": post}
    )


@router.get("/create", response_class=HTMLResponse)
def create_post_form(
    request: Request,
    current_user: CurrUser
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не авторизованы."
        )
    return templates.TemplateResponse(
        "partials/post_create.html",
        {"request": request, "current_user": current_user}
    )


@router.post("/create", response_class=RedirectResponse)
def create_post_submit(
    db_session: DbSession,
    current_user: CurrUser,
    title: str = Form(...),
    content: str = Form(...)
):
    post_in = PostCreate(title=title, content=content)
    create(
        db_session=db_session,
        post_in=post_in,
        user_id=current_user.id
    )
    return RedirectResponse("/posts", status_code=303)
