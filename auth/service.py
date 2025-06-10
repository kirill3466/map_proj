from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import User
from .schema import UserCreate, UserUpdate


def get(*, db_session: Session, user_id: int) -> Optional[User]:
    return db_session.query(User).filter(User.id == user_id).one_or_none()


def get_by_email(*, db_session: Session, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).one_or_none()


def create(*, db_session: Session, user_create: UserCreate) -> User:
    password = bytes(user_create.password, "utf-8")
    user = User(
        **user_create.model_dump(
            exclude={"password", "role"},
        ),
        password=password
    )
    db_session.add(user)
    db_session.commit()
    return user


def get_or_create(*, db_session: Session, user_create: UserCreate) -> User:
    user = get_by_email(db_session=db_session, email=user_create.email)
    if not user:
        try:
            user = create(db_session=db_session, user_create=user_create)
        except IntegrityError:
            db_session.rollback()
            # log exception here
    return user


def update(
    *,
    db_session: Session,
    user: User,
    user_update: UserUpdate
) -> User:
    user_data = user.dict()
    update_data = user_update.model_dump(
        exclude={"password", "role"},
        exclude_defaults=True
    )
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    if user_update.password:
        # print(user_update.password)
        # password = bytes(user_update.password, "utf-8")
        user.password = user_update.password

    db_session.commit()
    return user
