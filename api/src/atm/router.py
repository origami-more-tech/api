import json
from fastapi import APIRouter
from contstants import Collection
from atm.model import Atm
from typing import List, Dict
from fastapi.exceptions import HTTPException


router = APIRouter()
router.tags = [Collection.atms]


@router.get("/all")
async def get_atms(offset: int = 0, limit: int = 0) -> List[Atm]:
    with open("atms.json", encoding="utf-8") as json_file:
        atms = json.load(json_file)[offset : (offset + limit) if limit > 0 else None]
        atms = [Atm(**item) for item in atms]
        return atms


@router.get("/{id}")
async def get_atm_by_id(id: str) -> Atm:
    with open("atms.json", encoding="utf-8") as json_file:
        atms: List[Dict] = json.load(json_file)
        for atm in atms:
            if atm["id"] == id:
                return Atm(**atm)
    raise HTTPException(status_code=404, detail=f"Atm with {id} not found")
