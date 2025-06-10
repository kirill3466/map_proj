from typing import Optional

from sqlalchemy.orm import Session

import settings

from .models import Parcel
from .schema import ParcelCreate, ParcelUpdate

full_code = settings.PARCEL_FULL_CODE


def get(*, db_session, parcel_id: int) -> Optional[Parcel]:
    code = f"{full_code}{parcel_id}"
    return db_session.query(Parcel).filter(
        Parcel.cadastral_code == code
    ).one_or_none()


def get_all(*, db_session) -> list[Parcel]:
    parcels = db_session.query(Parcel).all()
    return parcels


def get_by_cadastral_code(
    *,
    db_session: Session,
    code: str
) -> Optional[Parcel]:
    query = db_session.query(Parcel).filter(Parcel.cadastral_code == code)
    return query.one_or_none()


def get_by_code_id(
    *,
    db_session: Session,
    code_id: int
) -> Optional[Parcel]:
    query = db_session.query(Parcel).filter(Parcel.code_id == code_id)
    return query.one_or_none()


def create(*, db_session, parcel: ParcelCreate) -> Parcel:
    parcel = Parcel(**parcel.model_dump())
    db_session.add(parcel)
    db_session.commit()
    db_session.refresh(parcel)
    return parcel


def update(
    *,
    db_session: Session,
    parcel: Parcel,
    parcel_update: ParcelUpdate
) -> Parcel:
    update_data = parcel_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(parcel, field, value)
    db_session.commit()
    db_session.refresh(parcel)
    return parcel


def delete(*, db_session: Session, parcel_id: int) -> None:
    parcel = db_session.query(Parcel).filter(Parcel.id == parcel_id).first()
    db_session.delete(parcel)
    db_session.commit()
