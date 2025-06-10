from typing import Optional

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from .models import Notification
from .schema import NotificationCreate


def get(
    *,
    db_session: Session,
    notification_id: int
) -> Optional[Notification]:
    return db_session.query(
        Notification
    ).filter(Notification.id == notification_id).one_or_none()


def get_my_notifications(
    *,
    db_session: Session,
    user_id: int
) -> list[Notification]:
    return db_session.query(
        Notification
    ).filter(Notification.user_id == user_id).all()


def create(
    *,
    db_session: Session,
    notification_in: NotificationCreate
) -> Notification:
    notification = Notification(**notification_in.model_dump())
    db_session.add(notification)
    db_session.commit()
    db_session.refresh(notification)
    return notification


# def update(
#     *,
#     db_session: Session,
#     notification: Notification,
#     notification_in: NotificationUpdate
# ) -> Notification:
#     update_data = notification_in.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(notification, field, value)
#     db_session.commit()
#     return notification


def delete(
    *,
    db_session: Session,
    notification_id: int
):
    notification = get(db_session=db_session, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено."
        )
    db_session.delete(notification)
    db_session.commit()
