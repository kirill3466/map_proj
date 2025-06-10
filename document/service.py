import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from .models import Document
from .schema import DocumentUpdate


def create(
    *,
    db_session: Session,
    filename: str,
    user_id: int,
    parcel_id: int = None
) -> Document:
    db_document = Document(
        filename=filename,
        user_id=user_id,
        parcel_id=parcel_id
    )
    db_session.add(db_document)
    db_session.commit()
    db_session.refresh(db_document)
    return db_document


def load_to_storage(file: UploadFile) -> str:
    file_location = f"static/documents/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location


def get(*, db_session: Session, document_id: int) -> Document:
    return db_session.query(Document).filter(
        Document.id == document_id
    ).first()


def get_by_filename(*, db_session: Session, filename: str) -> Document:
    return db_session.query(Document).filter(
        Document.filename == filename
    ).first()


def get_documents(*, db_session: Session, user_id: int) -> list[Document]:
    return db_session.query(Document).filter(
        Document.user_id == user_id
    ).all()


def delete(*, db_session: Session, document_id: int) -> None:
    document = db_session.query(Document).filter(
        Document.id == document_id
    ).first()
    if document:
        db_session.delete(document)
        db_session.commit()


def delete_from_storage(filename: str) -> None:
    file_location = f"static/documents/{filename}"
    if file_location:
        os.remove(file_location)


def update(
    *,
    db_session: Session,
    document_id: int,
    document_update: DocumentUpdate
) -> Document:
    document = db_session.query(Document).filter(
        Document.id == document_id
    ).first()
    if not document:
        return None
    if document_update.filename is not None:
        document.filename = document_update.filename
    db_session.commit()
    db_session.refresh(document)
    return document


def update_in_storage(filename: str, new_filename: str) -> None:
    file_location = f"static/documents/{filename}"
    new_file_location = f"static/documents/{new_filename}"
    if file_location:
        os.rename(file_location, new_file_location)
