import json
import pandas as pd
from typing import List

from fastapi.encoders import jsonable_encoder


def write_models_to_json(file: str, models):
    with open(file, "w") as json_file:
        dump = json.dumps(
            [jsonable_encoder(model) for model in models], ensure_ascii=False
        )
        json_file.write(dump)


def rank(offices: List[dict]) -> List[dict]:
    offices_df = pd.DataFrame(offices)
    offices_df["workload"] = offices_df["people"] / offices_df["windows"]
    offices_df = offices_df.sort_values(
        ["distance", "workload"], ascending=[True, True]
    )
    offices_df.loc[
        (0 <= offices_df["workload"]) & (offices_df["workload"] <= 2), "workload_type"
    ] = 0
    offices_df.loc[
        (2 < offices_df["workload"]) & (offices_df["workload"] <= 3.5), "workload_type"
    ] = 1
    offices_df.loc[3.5 < offices_df["workload"], "workload_type"] = 2
    offices = offices_df.to_dict(orient="records")
    return offices
