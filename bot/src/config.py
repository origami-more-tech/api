import os
from enum import Enum

TOKEN = str(os.getenv("BOT_TOKEN"))


class Collection(str, Enum):
    Chat = "chat"
