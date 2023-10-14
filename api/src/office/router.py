import json
import pandas as pd
from firestore import firestore
from fastapi import APIRouter
from contstants import Collection
from office.model import Office
from typing import List


router = APIRouter()
router.tags = [Collection.office]

def rank(offices: List[dict]) -> List[dict]:
    offices_df = pd.DataFrame(offices)
    offices_df['workload'] = offices_df['people'] / offices_df['windows']
    offices_df = offices_df.sort_values(['distance', 'workload'], ascending=[True, True])
    offices_df.loc[(0 <= offices_df['workload']) & (offices_df['workload'] <= 2), 'workload_type'] = 0
    offices_df.loc[(2 < offices_df['workload']) & (offices_df['workload'] <= 3.5), 'workload_type'] = 1
    offices_df.loc[3.5 < offices_df['workload'], 'workload_type'] = 2
    offices = offices_df.to_dict(orient='records')
    return offices

@router.get("/all")
async def get_all_offices(offset: int = 0, limit: int = 0) -> List[Office]:
    with open("offices.json", encoding='utf-8') as json_file:
        offices = json.load(json_file)
        offices = rank(offices)
        offices = [Office(**item) for item in offices][offset : (offset + limit) if limit > 0 else None]
        return offices
