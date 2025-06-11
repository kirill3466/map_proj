
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from pydantic_core import PydanticCustomError
from starlette.responses import RedirectResponse

from db.core import DbSession
from exceptions import (
    InvalidConfigError,
)
from settings import templates

from .auth import CurrUser, authenticate_user, create_token
from .permissions import RoleChecker
from .schema import UserCreate, UserRead, UserUpdate
from .service import create, get, get_by_email, update

user_router = APIRouter()
auth_router = APIRouter()


# TODO добавить success после регистрации шаблоны


@auth_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@auth_router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    db_session: DbSession,
    email: str = Form(...),
    password: str = Form(...)
):
    user_create = UserCreate(email=email, password=password)
    user = get_by_email(db_session=db_session, email=user_create.email)
    if user:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error_msg": "Пользователь с таким email уже существует"
            },
        )
    user = create(db_session=db_session, user_create=user_create)
    return RedirectResponse("/login", status_code=303)
    # return templates.TemplateResponse(
    #     "success.html",
    #     {
    #         "request": request,
    #         "success_msg": "Регистрация успешна!",
    #         "path_route": "auth/login",
    #         "path_msg": "Нажмите здесь, чтобы войти!",
    #     },
    # )


@auth_router.get("/login", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login", response_class=HTMLResponse)
async def login(
    db_session: DbSession,
    email: str = Form(...),
    password: str = Form(...),
):
    try:
        user = authenticate_user(
            db_session, email, password
        )
        if user is None:
            raise HTTPException(status_code=400, detail="Ошибка входа")
        access_token = create_token(
            data={"sub": user.email}, expires_delta=timedelta(minutes=60)
        )
        response = RedirectResponse("/", status_code=303)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@user_router.post("", response_model=UserRead)
def create_user(*, user_create: UserCreate, db_session: DbSession):
    user = get_by_email(db_session=db_session, email=user_create.email)
    if user:
        raise PydanticCustomError(
            InvalidConfigError(
                msg="Пользователь с таким email уже существует"
            ),
            model=UserCreate,
        )
    user = create(db_session=db_session, user_create=user_create)
    return user


@user_router.get("/{user_id}", response_model=UserRead)
def get_user(
    *,
    user_id: int,
    db_session: DbSession,
    current_user: CurrUser
):
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Пользователь с данным id не найден."}],
        )
    return user


@user_router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    user_id: int,
    user_update: UserUpdate,
    db_session: DbSession,
    current_user: CurrUser
):
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Пользователь с данным id не найден."}],
        )
    user = update(db_session=db_session, user=user, user_update=user_update)
    return user


@auth_router.get(
    "/me",
    response_model=UserRead,
    dependencies=[
        Depends(RoleChecker(allowed_roles=["admin", "user", "owner"]))
    ],
)
async def get_me(
    current_user: CurrUser
):
    return current_user
