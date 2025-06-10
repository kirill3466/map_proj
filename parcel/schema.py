from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field


class ParcelBase(BaseModel):
    id: int
    owner_id: Optional[int] = None
    kvartal: str
    cadastral_code: str
    area_value: float
    date_cost: datetime
    permitted_use: str
    readable_address: str
    ownership_type: str
    status: str
    longitude: float
    latitude: float
    cad_cost: float
    description: Optional[str] = None


class ParcelCreate(BaseModel):
    # owner id only for test
    owner_id: Optional[int] = None
    cadastral_code: str
    longitude: float
    latitude: float
    cad_cost: float
    description: Optional[str] = None


class ParcelUpdate(BaseModel):
    cadastral_code: Optional[str] = Field(None, nullable=True)
    owner_id: Optional[int] = None
    date_cost: datetime = None
    cad_cost: Optional[float]
    description: Optional[str] = Field(None, nullable=True)
