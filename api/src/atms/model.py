from uuid import uuid4
from pydantic import BaseModel, Field
from typing import List


class Service(BaseModel):
    serviceCapability: str | None
    serviceActivity: str | None


class Atms(BaseModel):
    id: str = Field(default=str(uuid4()))
    address: str
    latitude: str
    longitude: str
    allDay: str
    openHoursIndividual: List[Service]
