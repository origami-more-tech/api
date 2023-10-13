import json
from fastapi import APIRouter
from contstants import Collection
from atms.model import Atms
from typing import List


router = APIRouter()
router.tags = [Collection.atms]


@router.get("/atms")
async def get_atms(offset: int = 0, limit: int = 10) -> List[Atms]:
    with open("atms.json") as json_file:
        atms = json.load(json_file)[offset : offset + limit]
        atms = [Atms(**item) for item in atms]
        return atms
