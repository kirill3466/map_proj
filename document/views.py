import os

from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse

from auth.auth import CurrUser
from db.core import DbSession
from parcel.service import get as get_parcel
from parcel.views import router as parcel_router
from settings import templates

from .schema import Document, DocumentRead, DocumentUpdate
from .service import (
    create,
    delete,
    delete_from_storage,
    get,
    get_by_filename,
    get_documents,
    load_to_storage,
    update,
    update_in_storage,
)

router = APIRouter()


@parcel_router.post("/{parcel_id}/upload/", response_class=HTMLResponse)
async def upload_document_to_parcel(
    request: Request,
    parcel_id: int,
    current_user: CurrUser,
    db: DbSession,
    file: UploadFile = File(...),
):
    parcel = get_parcel(db_session=db, parcel_id=parcel_id)
    if not parcel or (parcel.owner_id != current_user.id and current_user.role != 'admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому участку"
        )
    document = create(
        db_session=db,
        user_id=current_user.id,
        # ВАЖНО! вставляется айди, а поиск по код айди
        parcel_id=parcel.id,
        filename=file.filename
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании документа"
        )
    try:
        load_to_storage(file)
    except Exception as e:
        delete(db_session=db, document_id=document.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сохранения файла: {str(e)}"
        )
    return templates.TemplateResponse(
        "partials/parcel.html",
        {"request": request, "parcel": parcel}
    )


@router.post("/upload/", response_model=DocumentRead)
async def upload_document(
    current_user: CurrUser,
    db: DbSession,
    file: UploadFile = File(...),
):
    doc = get_by_filename(db_session=db, filename=file.filename)
    if doc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": "Документ с таким названием уже есть"}],
        )
    document = create(
        db_session=db,
        user_id=current_user.id,
        filename=file.filename,
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{"msg": "Ошибка при создании документа"}],
        )
    else:
        load_to_storage(file)
    return document


@router.get("", response_model=list[Document])
async def read_documents(
    current_user: CurrUser,
    db: DbSession,
):
    documents = get_documents(db_session=db, user_id=current_user.id)
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Документы не найдены"}],
        )
    return documents


@router.get("/{document_id}", response_model=Document)
async def read_document(
    document_id: int,
    current_user: CurrUser,
    db: DbSession
):
    document = get(db_session=db, document_id=document_id)
    if not document or document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Документ не найден"}],
        )
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: CurrUser,
    db: DbSession,
):
    document = get(db_session=db, document_id=document_id)
    if not document or document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Документ не найден"}],
        )
    delete(db_session=db, document_id=document_id)
    delete_from_storage(document.filename)
    return {"msg": "Документ успешно удален"}


@router.put("/{document_id}", response_model=Document)
async def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    current_user: CurrUser,
    db: DbSession,
):
    document = get(db_session=db, document_id=document_id)
    if not document or document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Документ не найден"}],
        )

    original_filename = document.filename
    file_extension = os.path.splitext(original_filename)[1]
    new_filename = document_update.filename

    if new_filename and not new_filename.endswith(file_extension):
        new_filename += file_extension

    update_in_storage(original_filename, new_filename)

    document_update.filename = new_filename
    updated_document = update(
        db_session=db,
        document_id=document_id,
        document_update=document_update
    )

    if not updated_document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{"msg": "Ошибка при обновлении документа"}],
        )

    return updated_document
