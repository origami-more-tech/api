import json

from fastapi.encoders import jsonable_encoder


def write_models_to_json(file: str, models):
    with open(file, "w") as json_file:
        dump = json.dumps(
            [jsonable_encoder(model) for model in models], ensure_ascii=False
        )
        json_file.write(dump)
