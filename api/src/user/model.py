from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: str = Field(default=str(uuid4()))
    userName: str = Field(default=str("evgeniybenedict"))
    firstName: str = Field(default=str("Евгений"))
    surName: str = Field(default=str("Бенедиктус"))
    phoneNumber: str = Field(default=str("89538402696"))
    email: EmailStr = Field(default="benedictus@mail.ru")
    password: str = Field(default=str("vtbBankVerify123"))
    createdAt: str = Field(default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
