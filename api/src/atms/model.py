from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class Atms(BaseModel):
    address: str = Field(default=str(uuid4()))
    latitude: str = Field(default=str("evgeniybenedict"))
    longitude: str = Field(default=str("Евгений"))
    allDay: str = Field(default=str("Бенедиктус"))
    services: str = Field(default=str("89538402696"))
    email: EmailStr = Field(default="benedictus@mail.ru")
    password: str = Field(default=str("vtbBankVerify123"))
    createdAt: str = Field(default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))