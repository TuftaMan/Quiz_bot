from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

async def create_keyboard_start():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Начать игру'))
    builder.row(KeyboardButton(text='Статистика'))
    return builder.as_markup(resize_keyboard=True)

async def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()
    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        builder.add(InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'
            callback_data=f"answer/{option}")
        )
    #Выводи по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()