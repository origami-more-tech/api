from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN
from firestore import Firestore

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
firestore = Firestore()
scheduler = AsyncIOScheduler()
