from enum import Enum


class Collection(str, Enum):
    user = "user"
    office = "office"
    atms = "atms"
