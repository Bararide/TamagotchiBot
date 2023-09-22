import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_KEY = ('6451676145:AAFcWrDgRersroao4CPTUdB8Sno2PSN72Po')
bot = aiogram.Bot(API_KEY)
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)