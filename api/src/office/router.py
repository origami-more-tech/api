import json
from firestore import firestore
from fastapi import APIRouter
from contstants import Collection
from office.model import Office
from typing import List


router = APIRouter()
router.tags = [Collection.office]


@router.get("/all")
async def get_all_offices(offset: int = 0, limit: int = 0) -> List[Office]:
    with open("offices.json") as json_file:
        offices = json.load(json_file)[offset : (offset + limit) if limit > 0 else None]
        offices = [Office(**item) for item in offices]
        return offices
