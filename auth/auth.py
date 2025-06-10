from datetime import datetime, timedelta
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from db.core import DbSession
from settings import JWT_ALG, JWT_EXP, JWT_SECRET

from .models import User
from .schema import TokenData
from .security import validate_password
from .service import get_by_email

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=[{"msg": "Неверная почта или пароль"}]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(
    db_session: DbSession,
    email: str,
    password: str
) -> User:
    user = get_by_email(db_session=db_session, email=email)
    if not user:
        return False
    if not validate_password(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(JWT_EXP)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)
    return encoded_jwt


async def get_current_user(
    db_session: DbSession,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_by_email(db_session=db_session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


CurrUser = Annotated[User, Depends(get_current_user)]


def get_current_role(current_user: CurrUser) -> str:
    user = get_current_user(
        token=current_user.token,
        db_session=current_user.db_session
    )
    return user.role
