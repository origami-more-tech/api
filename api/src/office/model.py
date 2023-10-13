from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Union, List


class OpenHours(BaseModel):
    days: str
    hours: str | None


class Office(BaseModel):
    id: str = Field(default=str(uuid4()))
    salePointName: str
    address: str
    rko: str | None
    officeType: str
    salePointFormat: str
    suoAvailability: str | None
    hasRamp: str | None
    latitude: float
    longitude: float
    metroStation: str | None
    distance: int
    kep: bool | None
    myBranch: bool
    openHours: List[OpenHours]
    openHoursIndividual: List[OpenHours]
