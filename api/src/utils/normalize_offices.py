import json

from uuid import uuid4
from office.model import Office, OpenHours
from typing import List
from utils.helpers import write_models_to_json


def transform_open_hours(openHours: List[OpenHours]) -> List[OpenHours]:
    transformd = []
    days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
    for item in openHours:
        if "-" in item.days:
            start, end = item.days.split("-")
            start_idx = days.index(start)
            end_idx = days.index(end)
            for i in range(start_idx, end_idx + 1):
                transformd.append(OpenHours(days=days[i], hours=item.hours))
        elif "," in item.days:
            days = item.days.split(",")
            for day in days:
                transformd.append(OpenHours(days=day, hours=item.hours))
        elif item.days == "в":
            transformd.append(OpenHours(days="вс", hours=item.hours))
        else:
            transformd.append(item)
    return transformd


def transform_address(address: str) -> str:
    try:
        return address[address.index("г") :]
    except ValueError:
        return address[address.index(",")]


with open("offices.json", "r") as json_file:
    offices = json.load(json_file)
    offices = [Office(**(item | {"id": str(uuid4())})) for item in offices]
    for office in offices:
        office.address = transform_address(office.address)
        office.openHours = transform_open_hours(office.openHours)
        office.openHoursIndividual = transform_open_hours(office.openHoursIndividual)
write_models_to_json("offices.json", offices)
