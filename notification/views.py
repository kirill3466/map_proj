# views.py
from fastapi import APIRouter, HTTPException, status

from auth.auth import CurrUser
from db.core import DbSession

from .schema import NotificationCreate, NotificationRead
from .service import create, delete, get, get_my_notifications

router = APIRouter()


@router.get("/{notification_id}", response_model=NotificationRead)
def get_notification(db_session: DbSession, notification_id: int):
    notification = get(
        db_session=db_session,
        notification_id=notification_id
    )
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено."
        )
    return notification


@router.get("", response_model=list[NotificationRead])
def get_all_notifications(db_session: DbSession, current_user: CurrUser):
    return get_my_notifications(db_session=db_session, user_id=current_user.id)


@router.post("", response_model=NotificationRead)
def create_notification(
    db_session: DbSession,
    notification_in: NotificationCreate,
):
    return create(db_session=db_session, notification_in=notification_in)


# @router.put("/{notification_id}", response_model=NotificationRead)
# def update_notification(
#     db_session: DbSession,
#     notification_id: int,
#     notification_in: NotificationUpdate
# ):
#     notification = get(
    # db_session=db_session,
    # notification_id=notification_id
    # )
#     if not notification:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Уведомление не найдено."
#         )
#     return update(
#         db_session=db_session,
#         notification=notification,
#         notification_in=notification_in
#     )


@router.delete("/{notification_id}", response_model=None)
def delete_notification(db_session: DbSession, notification_id: int):
    notification = get(db_session=db_session, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено."
        )
    delete(db_session=db_session, notification_id=notification_id)
