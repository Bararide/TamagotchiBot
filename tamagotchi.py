from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

import random
import asyncio

from main import bot, dp
from menu_manager import cry_list, menu, new_pet, choose

from pet_container import Pet
from database_manager import database_handler
from travel_manager import travel_helper

pet = Pet()
dh = database_handler()
th = travel_helper()

class UserStates(StatesGroup):
    NAME    = State()
    REST    = State()
    ADD     = State()
    GEO     = State()
    ADDRESS = State()

def check_animal(text: str) -> str:
    if text == "dog":
        return "Собака"
    elif text == "cat":
        return "Кот"
    elif text == "hamster":
        return "Хомяк"
    elif text == "snake":
        return "Питон"
    else:
        return "Черепаха"
    
def check_new_pet(text: str) -> bool:
    if text == 'new':
        return True
    else:
        return False
    
def check_choose_answer(text: str) -> bool:
    if text == 'yes':
        return True
    else:
        return False

@dp.message_handler(Command('start'))
async def start(message: types.Message, state: FSMContext):
    try:
        print(message.from_user.id)
        if(dh.check(message.from_user.id) == True):
            await bot.send_message(message.from_user.id, 'Заведите питомца', reply_markup = cry_list)
        else:
            await bot.send_message(message.from_user.id, 'У вас уже есть питомец, вернитесь к нему', reply_markup = new_pet)
            dh.create_pet(pet, message.from_user.id)
    except Exception as e:
        await message.reply(f'{e} Bot is not available. Link ->t.me/testmyfirstbot')

pet_answer = '''Вы завели питомца, молодцы! И этот питомец - {sort}. \n Давайте дадим вашему питомцу имя, как его зовут?'''

@dp.callback_query_handler(text_contains='nn_')
async def return_to_pet(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    result = check_new_pet(call.data[3:])
    if(result == False):
        await bot.send_message(call.from_user.id, 'Вы вернулись к своему питомцу', reply_markup = menu)
    else:
        await bot.send_message(call.from_user.id, 'Вы выбрали завести ещё одного питомца', reply_markup = cry_list)        

@dp.callback_query_handler(text_contains='cc_')
async def choose_pet(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        button_text = check_animal(call.data[3:])
        pet.owner = call.from_user.id
        pet.animal = button_text
        await UserStates.NAME.set()
        await bot.send_message(call.from_user.id, pet_answer.format(sort = button_text))
    except Exception as e:
        await bot.send_message(call.from_user.id, f"Error: {e}")

@dp.message_handler(state=UserStates.NAME)
async def choose_name(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, "Какое необычное имя, но весьма подходящее для вашего питомца", reply_markup=menu)
        pet.pet_name = message.text
        pet.health = int(random.randint(60, 85))
        dh.create(pet)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.from_user.id, f"Error {e}")

@dp.message_handler()
async def message_helper(message: types.Message):
    try:
        if pet.latitude == None:
            dh.create_pet(pet, message.from_user.id)

        if message.text == "Паспорт":
            if pet.owner != message.from_user or hasattr(pet, 'latitude'):
                print('ok')
                dh.create_pet(pet, message.from_user.id)

            await bot.send_message(message.from_user.id, f"Вот паспорт вашего питомца:\nИмя: {pet.pet_name} \nВид питомца: {pet.animal} \nСостояние здоровья: {pet.health}")  

        elif message.text == "Погулять":
            if pet.owner != message.from_user.id:
                dh.create_pet(pet, message.from_user.id)  

            if hasattr(pet, 'latitude') and not pet.latitude:
                await UserStates.GEO.set()             
                await bot.send_message(message.from_user.id, "Можно ли обрабатывать ваши геоданные?", reply_markup=choose)
            else:
                await bot.send_message(message.from_user.id, "Вы вышли на прогулку со своим питомцем, молодцы!")
        else:
            await message.reply("Извините,я не знаю, к чему относится это сообщение")
    except Exception as e:
        await bot.send_message(message.from_user.id, f"Error {e}")

@dp.message_handler(text = "Нет", state=UserStates.GEO)
async def choose_geoposition_no(call: types.Message, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message_id)
        await bot.send_message(call.from_user.id, f"Как считаете нужным, эта функция будет отключена", reply_markup=menu)
    except Exception as e:
        print(e)
    
    await state.finish()

@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=UserStates.GEO)
async def choose_geoposition(call: types.Message, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message_id)
        pet.latitude = call.location.latitude
        pet.longitude = call.location.longitude
        dh.include_coordinate(pet)
        await bot.send_message(call.from_user.id, f"Спасибо за сотрудничество. Выберете следующее действие", reply_markup=menu)

    except Exception as e:
        print(e)
    
    await state.finish()

executor.start_polling(dp, skip_updates = True)