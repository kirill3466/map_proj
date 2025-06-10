from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from auth.auth import CurrUser
from db.core import DbSession
from settings import templates

from .schema import ParcelBase, ParcelCreate, ParcelUpdate
from .service import (
    create,
    delete,
    get,
    get_all,
    get_by_cadastral_code,
    update,
)

router = APIRouter()


@router.get("/{parcel_id}", response_model=ParcelBase)
def get_parcel(
    request: Request,
    db_session: DbSession,
    current_user: CurrUser,
    parcel_id: int,
):
    parcel = get(db_session=db_session, parcel_id=parcel_id)
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Участок не найден"}],
        )
    return templates.TemplateResponse(
        "partials/parcel.html",
        {"request": request, "parcel": parcel}
    )


@router.get("", response_class=HTMLResponse)
def get_all_parcels(
    request: Request,
    current_user: CurrUser,
):
    db_session = request.state.db
    parcels = get_all(db_session=db_session)
    return templates.TemplateResponse(
        "partials/parcels.html",
        {"request": request, "parcels": parcels}
    )


@router.post("", response_model=ParcelCreate)
def create_parcel(
    *,
    db_session: DbSession,
    parcel_create: ParcelCreate,
    current_user: CurrUser
):
    parcel = get_by_cadastral_code(
        db_session=db_session,
        code=parcel_create.cadastral_code
    )
    if parcel:
        raise HTTPException(
            status_code=status.HTTP_401_BAD_REQUEST,
            detail=[{"msg": "Участок с таким кодом уже существует"}],
        )
    parcel = create(db_session=db_session, parcel=parcel_create)
    return parcel


@router.put("/{parcel_id}", response_model=ParcelUpdate)
def update_parcel(
    *,
    db_session: DbSession,
    parcel_id: int,
    parcel_update: ParcelUpdate,
    current_user: CurrUser
) -> ParcelUpdate:
    parcel = get(db_session=db_session, parcel_id=parcel_id)
    # if cadastral code already used
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Участок не найден"}],
        )
    parcel = update(
        db_session=db_session,
        parcel=parcel,
        parcel_update=parcel_update
    )
    return parcel


@router.delete("/{parcel_id}")
def delete_parcel(
    *,
    db_session: DbSession,
    parcel_id: int,
    current_user: CurrUser
):
    parcel = get(db_session=db_session, parcel_id=parcel_id)
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Участок не найден"}],
        )
    delete(db_session=db_session, parcel_id=parcel_id)
