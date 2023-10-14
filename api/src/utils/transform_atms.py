import json
from utils.helpers import write_models_to_json
from atm.model import Atm
from uuid import uuid4


with open("atms.json", "r") as json_file:
    data = json.load(json_file)
    atms = data["atms"]

    for atm in atms:
        services = atm["services"]
        new_services = []
        for service_name, service in services.items():
            new_services.append({"name": service_name} | service)
        atm["services"] = new_services

    atms = [Atm(**(item | {"id": str(uuid4())})) for item in atms]
write_models_to_json("atms.json", atms)
