from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from db.core import Base


class Parcel(Base):
    __tablename__ = 'parcels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(
        ForeignKey('users.id'),
        nullable=True
    )
    cadastral_code = Column(String, unique=True)
    code_id = Column(String, nullable=True)
    kvartal = Column(String, nullable=True)
    area_value = Column(Float, nullable=True)
    date_cost = Column(Date, nullable=True)
    cad_cost = Column(Float, nullable=True)
    permitted_use = Column(String, nullable=True)
    readable_address = Column(String, nullable=True)
    ownership_type = Column(String, nullable=True)
    status = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    description = Column(String, nullable=True)

    owner = relationship("User", back_populates="parcels")
    documents = relationship("Document", back_populates="parcel")
