from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
from app.quiz import new_quiz, get_quiz_index, update_quiz_index, quiz_data, get_question, update_quiz_result
from app.database.table import get_quiz_result, get_quiz_index, update_quiz_result, update_quiz_index

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот для проведения квиза. Введите /quiz, чтобы начать.",
                         reply_markup=await kb.create_keyboard_start())

@router.message(F.text=='Начать игру')
@router.message(Command('quiz'))
async def cmd_quiz(message: Message):
    await message.answer('Давайте начнем квиз!', reply_markup=ReplyKeyboardRemove())
    #Запускаем новый квиз
    await new_quiz(message)

@router.message(F.text=='Статистика')
async def cmd_quiz(message: Message):
    result = await get_quiz_result(message.from_user.id)
    await message.answer(f'Твой счет - {result}')


@router.callback_query(F.data.startswith('answer/'))
async def get_answer(callback: CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    user_answer = callback.data.split('/')[1]
    await callback.message.answer(f'Вы выбрали - {user_answer}')
    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    result = await get_quiz_result(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    right_answer = quiz_data[current_question_index]['options'][correct_option]
    print(user_answer, correct_option, right_answer)

    if user_answer == right_answer:
        await callback.answer('Верно!')
        await callback.message.answer('Верно!')
        result = await get_quiz_result(callback.from_user.id) + 1
        result = await update_quiz_result(callback.from_user.id, result)
    else:
        await callback.answer('Неверно!')
        await callback.message.answer(
            f"Неправильно. Правильный ответ: {right_answer}")
        # Обновление номера текущего вопроса в базе данных
    await callback.answer('')
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        result = await get_quiz_result(callback.from_user.id)
        await callback.message.answer("Это был последний вопрос. Квиз завершен!\n"
                                      f"Твой результат - {result} очков")