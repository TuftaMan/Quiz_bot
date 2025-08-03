from app.database.table import update_quiz_index, get_quiz_index, update_quiz_result, get_quiz_result
import app.keyboards as kb


# Структура квиза
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для сравнения двух значений?',
        'options': ['=', '==', '!=', 'is'],
        'correct_option': 1
    },
    {
        'question': 'Какой метод используется для добавления элемента в список?',
        'options': ['append()', 'add()', 'insert()', 'push()'],
        'correct_option': 0
    },
    {
        'question': 'Что вернёт выражение `len("Python")`?',
        'options': ['5', '6', '"Python"', 'Ошибка'],
        'correct_option': 1
    },
    {
        'question': 'Какой тип данных у переменной: `x = 3.14`?',
        'options': ['int', 'float', 'str', 'bool'],
        'correct_option': 1
    },
    {
        'question': 'Какая конструкция используется для обработки исключений?',
        'options': ['try-except', 'if-else', 'for-while', 'raise-pass'],
        'correct_option': 0
    },
    {
        'question': 'Что делает функция `range(5)`?',
        'options': ['Возвращает список от 1 до 5', 'Создает диапазон от 0 до 4', 'Создает кортеж', 'Ничего'],
        'correct_option': 1
    },
    {
        'question': 'Какой результат у выражения `bool(0)`?',
        'options': ['True', '0', 'False', 'None'],
        'correct_option': 2
    },
    {
        'question': 'Как объявить функцию в Python?',
        'options': ['function myFunc():', 'def myFunc():', 'func myFunc():', 'declare myFunc():'],
        'correct_option': 1
    },
    {
        'question': 'Что делает ключевое слово `return` в функции?',
        'options': ['Завершает программу', 'Выводит сообщение', 'Возвращает значение из функции', 'Создает переменную'],
        'correct_option': 2
    },
    {
        'question': 'Какой символ используется для написания комментариев в Python?',
        'options': ['#', '@', '$', '&'],
        'correct_option': 0
    },
    {
        'question': 'Какой метод строки делает все символы заглавными?',
        'options': ['upper()', 'capitalize()', 'title()', 'uppercase()'],
        'correct_option': 0
    },
]

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    result = 0
    await update_quiz_index(user_id, current_question_index)
    await update_quiz_result(user_id, result)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)


async def get_question(message, user_id):
    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=await kb.generate_options_keyboard(opts))
