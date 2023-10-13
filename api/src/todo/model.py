from uuid import uuid4
from typing import Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Todo(BaseModel):
    id: str = Field(default=str(uuid4()))
    label: str
    description: Optional[str]
    priority: Priority
    completed: bool = Field(default=False)
    createdAt: str = Field(default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    updatedAt: str = Field(default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


class CreateTodoDTO(BaseModel):
    label: str
    description: Optional[str]
    priority: Optional[Priority] = Field(default=Priority.medium)


class PatchTodoDTO(BaseModel):
    label: Optional[str]
    description: Optional[str] = Field(default=None)
    priority: Optional[Priority]
    completed: Optional[bool]
