from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

cb1 = InlineKeyboardButton(text = 'Собака', callback_data='cc_dog')
cb2 = InlineKeyboardButton(text = 'Кот', callback_data='cc_cat')
cb3 = InlineKeyboardButton(text = 'Хомяк', callback_data='cc_hamster')
cb4 = InlineKeyboardButton(text = 'Черепаха', callback_data='cc_turtle')
cb5 = InlineKeyboardButton(text = 'Питон', callback_data='cc_snake')

cry_list = InlineKeyboardMarkup(resize_keyboard=True).add(cb1, cb2, cb3, cb4, cb5)

b1 = KeyboardButton('Погулять')
b2 = KeyboardButton('Покормить')
b3 = KeyboardButton('Поиграть')
b4 = KeyboardButton('Проверить')
b5 = KeyboardButton('Паспорт')

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(b1, b2, b3, b4, b5)

c2 = InlineKeyboardButton(text = 'Мой питомец', callback_data='nn_return')

new_pet = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(c2)

c1 = KeyboardButton(text = 'Да', request_location = True)
c2 = KeyboardButton(text = 'Нет', request_location = False)

c3 = KeyboardButton(text = 'Да')
c4 = KeyboardButton(text = 'Нет')

choose = ReplyKeyboardMarkup(resize_keyboard=True).add(c3,c4)

choose_geo = ReplyKeyboardMarkup(resize_keyboard=True).add(c1,c2)