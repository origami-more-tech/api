from uuid import uuid4
from pydantic import BaseModel, Field
from typing import List


class Service(BaseModel):
    name: str
    serviceCapability: str | None
    serviceActivity: str | None


class Atm(BaseModel):
    id: str
    address: str
    latitude: float
    longitude: float
    allDay: bool
    services: List[Service]
