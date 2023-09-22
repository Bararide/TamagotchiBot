from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

import random

from main import bot, dp
from menu_manager import cry_list, menu, new_pet, choose, choose_geo

from database_manager import database_handler

dh = database_handler()

class UserStates(StatesGroup):
    NAME    = State()
    REST    = State()
    ADD     = State()
    GEO     = State()
    ADDRESS = State()
    PHOTO   = State()
    PHO     = State()

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
        if(dh.check_id(message.from_user.id) == False):
            await bot.send_message(message.from_user.id, 'Заведите питомца', reply_markup = cry_list)
        else:
            await bot.send_message(message.from_user.id, 'У вас уже есть питомец, вернитесь к нему', reply_markup = new_pet)
    except Exception as e:
        await message.reply(f'{e} Bot is not available. Link ->t.me/testmyfirstbot')

pet_answer = '''Вы завели питомца, молодцы! И этот питомец - {sort}. \nДавайте дадим вашему питомцу имя, как его зовут?'''

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
        dh.set_owner(call.from_user.id)
        dh.set_animal(button_text, call.from_user.id)
        await UserStates.NAME.set()
        await bot.send_message(call.from_user.id, pet_answer.format(sort = button_text))
    except Exception as e:
        await bot.send_message(call.from_user.id, f"Error choose pet: {e}")

@dp.message_handler(state=UserStates.NAME)
async def choose_name(message: types.Message):
    try:
        await UserStates.PHOTO.set()
        await bot.send_message(message.from_user.id, "Какое необычное имя, но весьма подходящее для вашего питомца.\nХотите прислать фотографию питомца?", reply_markup=choose)
        dh.set_name(message.text, message.from_user.id)
        dh.set_health(int(random.randint(60, 85)), message.from_user.id)
    except Exception as e:
        await bot.send_message(message.from_user.id, f"Error {e}")

@dp.message_handler(text = "Да", state=UserStates.PHOTO)
async def choose_photo_yes(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Как выглядит ваш питомец? Покажите фотографию питомца")
        await UserStates.PHO.set()
    except Exception as e:
        await bot.send_message(message.from_user.id, f"Error choose photo yes: {e}")   

@dp.message_handler(text = "Нет", state=UserStates.PHOTO)
async def choose_photo_no(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, "Жаль, вы не сможете посмотреть на своего питомца", reply_markup=menu)
        await state.finish()
    except Exception as e:
        await bot.send_message(message.from_user.id, f"Error choose photo no: {e}")

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=UserStates.PHO)
async def choose_photo(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[-1]
        if(dh.check_id(message.from_user.id) == True and dh.check_photo(message.from_user.id) == False):
            print('1')
            dh.set_photo(photo.file_id, message.from_user.id)
        else:
            await bot.send_message(message.from_user.id, "У вас уже есть фотография питомца", reply_markup=menu)
            await state.finish()
            

        await state.finish()
        await bot.send_message(message.from_user.id, "Спасибо за фотографию", reply_markup=menu)
    except Exception as e:
        print(e)

@dp.message_handler()
async def message_helper(message: types.Message):
    try:

        if message.text == "Паспорт" and dh.check_id(message.from_user.id):
            if dh.check_photo(message.from_user.id) is False:
                await bot.send_message(message.from_user.id, "Хотите прислать фотографию питомца?", reply_markup=choose)
                await UserStates.PHOTO.set()

                await bot.send_message(message.from_user.id,\
                                        f"Вот паспорт вашего питомца:\
                                        \nИмя: {str(dh.get_name(message.from_user.id))}\
                                        \nВид питомца: {dh.get_animal(message.from_user.id)}\
                                        \nСостояние здоровья: {dh.get_health(message.from_user.id)}")
            else:
                file_info = await bot.get_file(dh.get_photo(message.from_user.id))
                file_path = file_info.file_path
                photo_content = await bot.download_file(file_path)
                await bot.send_photo(message.from_user.id,\
                                     photo=photo_content, \
                                     caption=f"Вот паспорт вашего питомца:\
                                     \nИмя: {dh.get_name(message.from_user.id)}\
                                     \nВид питомца: {str(dh.get_animal(message.from_user.id))}\
                                     \nСостояние здоровья: {dh.get_health(message.from_user.id)}")           

        elif message.text == "Погулять":
            if dh.check_latitude(message.from_user.id) is False and dh.check_id(message.from_user.id) is not False:
                await UserStates.GEO.set()             
                await bot.send_message(message.from_user.id, "Можно ли обрабатывать ваши геоданные?", reply_markup=choose_geo)
            else:
                await bot.send_message(message.from_user.id, "Вы вышли на прогулку со своим питомцем, молодцы!")
        else:
            await message.reply("Извините, я не знаю, к чему относится это сообщение")
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
        dh.set_lotitude(call.location.latitude, call.from_user.id)
        print(call.location.latitude)
        dh.set_longitude(call.location.longitude, call.from_user.id)
        print(call.location.longitude)
        await bot.send_message(call.from_user.id, f"Спасибо за сотрудничество. Выберете следующее действие", reply_markup=menu)

    except Exception as e:
        print(e)
    
    await state.finish()

executor.start_polling(dp, skip_updates = True)