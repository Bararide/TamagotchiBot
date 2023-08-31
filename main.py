import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_KEY = ('YOUR_API_KEY')
bot = aiogram.Bot(API_KEY)
dp = aiogram.Dispatcher(bot, storage=storage)
