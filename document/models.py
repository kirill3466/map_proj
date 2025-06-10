from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.core import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    parcel_id = Column(Integer, ForeignKey('parcels.id'), nullable=True)

    owner = relationship("User", back_populates="documents")
    parcel = relationship("Parcel", back_populates="documents")
