import json

from uuid import uuid4
from office.model import Office, OpenHours
from typing import List
from fastapi.encoders import jsonable_encoder


def normalize_open_hours(openHours: List[OpenHours]) -> List[OpenHours]:
    normalized = []
    days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
    for item in openHours:
        if "-" in item.days:
            start, end = item.days.split("-")
            start_idx = days.index(start)
            end_idx = days.index(end)
            for i in range(start_idx, end_idx + 1):
                normalized.append(OpenHours(days=days[i], hours=item.hours))
        elif "," in item.days:
            days = item.days.split(",")
            for day in days:
                normalized.append(OpenHours(days=day, hours=item.hours))
        elif item.days == "в":
            normalized.append(OpenHours(days="вс", hours=item.hours))
        else:
            normalized.append(item)
    return normalized


def normalize_address(address: str) -> str:
    try:
        return address[address.index("г") :]
    except ValueError:
        return address[address.index(",")]


def normalize():
    with open("offices.json", "r") as json_file:
        offices = json.load(json_file)
        offices = [Office(**(item | {"id": str(uuid4())})) for item in offices]
        for office in offices:
            office.address = normalize_address(office.address)
            office.openHours = normalize_open_hours(office.openHours)
            office.openHoursIndividual = normalize_open_hours(
                office.openHoursIndividual
            )

    with open("offices.json", "w") as json_file:
        dump = json.dumps(
            [jsonable_encoder(office) for office in offices], ensure_ascii=False
        )
        json_file.write(dump)


normalize()
