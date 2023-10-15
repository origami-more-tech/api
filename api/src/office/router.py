import json
import pandas as pd
from fastapi import APIRouter
from contstants import Collection
from office.model import Office
from typing import List, Dict
from fastapi.exceptions import HTTPException
from utils.helpers import rank


router = APIRouter()
router.tags = [Collection.office]


@router.get("/all")
async def get_all_offices(offset: int = 0, limit: int = 0) -> List[Office]:
    with open("offices.json", encoding="utf-8") as json_file:
        offices = json.load(json_file)
        offices = rank(offices)
        offices = [Office(**item) for item in offices][
            offset : (offset + limit) if limit > 0 else None
        ]
        return offices


@router.get("/{id}")
async def get_office_by_id(id: str) -> Office:
    with open("offices.json", encoding="utf-8") as json_file:
        offices: List[Dict] = json.load(json_file)
        offices = rank(offices)
        for office in offices:
            if office["id"] == id:
                return Office(**office)
    raise HTTPException(status_code=404, detail=f"Office with {id} not found")
