from pydantic import BaseModel
from typing import List


class OpenHours(BaseModel):
    days: str
    hours: str | None


class Office(BaseModel):
    id: str
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
    people: int
    windows: int
    workload_type: int | None
