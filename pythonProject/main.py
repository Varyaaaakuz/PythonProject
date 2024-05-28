import telebot
from telebot import types
import wikipedia
import re
import random

bot = telebot.TeleBot('7061253604:AAFnjVwo7Og6v5QLTwufmqSMKoAPK4REoyg')

# Словарь для отслеживания состояния пользователя
user_state = {}
user_scores = {}
current_questions = {}
# Функция для проверки состояния пользователя
def get_user_state(message):
    return user_state.get(message.chat.id)

# Функция для установки состояния пользователя
def set_user_state(message, state):
    user_state[message.chat.id] = state

# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")

magic_ball_answers = [
    'Думаю, да!',
    'Не стоит.',
    'Я сомневаюсь в этом',
    'Вероятно, да',
    'Бесспорно',
    'Не могу сказать',
    'Не сейчас',
    'Лучше не надо',
    'Решительно, да!'
]
quiz_questions = {
    1: {
        'question': 'Столица Франции?',
        'answers': ['Москва', 'Париж', 'Берлин', 'Лондон'],
        'correct': 'Париж'
    },
    2: {
        'question': '2 + 2 * 2?',
        'answers': ['6', '8', '4', '2'],
        'correct': '6'
    },
    3: {
        'question': 'Сколько цветов в радуге?',
        'answers': ['6', '8', '4', '2'],
        'correct': '7'
    },
    4: {
        'question': 'Солнце - звезда или планета?',
        'answers': ['звезда', 'планета'],
        'correct': 'звезда'
    },
    5: {
        'question': 'Какого июня отмечается день защиты детей?',
        'answers': ['6', '8', '4', '2'],
        'correct': '1'
    },
    6: {
        'question': 'Какой овощ называют вторым хлебом?',
        'answers': ['морковь', 'капуста', 'огурец', 'картошка'],
        'correct': 'картошка'
    },
    7: {
        'question': 'В какой стране самое большое население мира?',
        'answers': ['Франция', 'Китай', 'Африка', 'Россия'],
        'correct': 'Китай'
    },
    8: {
        'question': 'С какого месяца начинается зима?',
        'answers': ['март', 'февраль', 'январь', 'декабрь'],
        'correct': 'декабрь'
    },
    9: {
        'question': 'За какой нотой идет "ми"?',
        'answers': ['до', 'соль', 'ля', 'ре'],
        'correct': 'ре'
    },
}
anecdotes = [
    'Принц поцеловал и разбудил принцессу, та вырубила его и переставила ещё на 5 минут.',
    'Россияне мечтали вернуться в СССР, когда было всё дешевое. И вот теперь у них много дешевой нефти, дешевого газа, дешевого золота и дешевых рублей.',
    'В сети ресторанов "Едим как дома" заставляют не только доедать всё до конца, но и мыть после этого посуду.',
    'Сегодня столько запретов... То нельзя, это нельзя...Я совсем растерялся. Опубликуйте, пожалуйста, список того, что можно. Он ведь небольшой получится. Заранее благодарю.',
    'Знаете, почему у Некрасова стихотворение называется «Размышления у парадного подъезда»? Он просто хотел продавать книги в обеих столицах.',
    'При виде дивана хочется лечь. При виде воды - пить. При виде еды - есть. А вот с работой что-то не так!',
    '- Дорогая, с 13 февраля по 9 марта меня будут искать враги. Прости, мы не сможем увидеться.',
    'Когда у меня спрашивают возраст, я отвечаю: я настолько старая, что помню, как HR называли "отдел кадров".',
    'Избегайте конфликтов с пожилыми людьми, с возрастом их все меньше пугает тюремное наказание.',
    'Думаю, чего день-то такой хороший... Потом вспомнил: я же на успокоительных.',
    'У меня сломался туалет. Звоню сантехнику, а он мне говорит: "Не ссы, ща приеду".',
    'После окончания курсов пекарей выдаётся корочка.',
    'Не хочу - это красивая, лаконичная фраза. Не понимаю, почему её перестали воспринимать как правильный аргумент, и нужно перечислять поводы, мотивы, прилагать пятистраничное эссе с объяснениями...',
    'С появлением робота-пылесоса в квартире стало значительно чище, так как приходится убирать с пола все разбросанные вещи.'
]
# Функция для стартовой команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Викторина')
    item2 = types.KeyboardButton('Анекдоты')
    item3 = types.KeyboardButton('Магический шар')
    item4 = types.KeyboardButton('Википедия')
    item5 = types.KeyboardButton('Факты')

    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Чем сегодня займемся?', reply_markup=markup)
    # Устанавливаем состояние пользователя как True, разрешая доступ к кнопкам
    set_user_state(message, True)

# Функция для получения текста из Wikipedia
def get_wiki_content(query):
    try:
        page = wikipedia.page(query)
        wikitext = page.content[:1000].split('.')
        wikitext = [sentence + '.' for sentence in wikitext if not '==' in sentence and len(sentence.strip()) > 3]
        wikitext = ' '.join(wikitext)
        wikitext = re.sub(r'\([^()]*\)', '', wikitext)
        wikitext = re.sub(r'\{[^\{\}]*\}', '', wikitext)
        return wikitext
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: get_user_state(message) and message.text == 'Википедия')
def handle_wikipedia_command(message):
    # Устанавливаем состояние пользователя как 'Википедия', разрешая поиск
    set_user_state(message, 'Википедия')
    bot.send_message(message.chat.id, 'Отправь мне слово для поиска в Википедии.')

# Обработчик текстовых сообщений для поиска в Википедии
@bot.message_handler(func=lambda message: get_user_state(message) == 'Википедия')
def handle_wikipedia_search(message):
    bot.send_message(message.chat.id, get_wiki_content(message.text))
    # После выполнения поиска сбрасываем состояние пользователя
    set_user_state(message, True)

# Обработчик текстовых сообщений для Магического шара
@bot.message_handler(func=lambda message: get_user_state(message) and message.text == 'Магический шар')
def handle_magic_ball_command(message):
    # Переводим состояние пользователя в режим Магического шара
    set_user_state(message, 'Магический шар')
    bot.send_message(message.chat.id, 'Спроси меня о чём угодно! Я помогу принять решение!')

# Обработчик текстовых сообщений для получения ответа от Магического шара
@bot.message_handler(func=lambda message: get_user_state(message) == 'Магический шар')
def handle_magic_ball_answer(message):
    # Проверяем, содержит ли сообщение вопросительный знак
    if '?' in message.text:
        # Отправляем случайный ответ из списка
        bot.send_message(message.chat.id, random.choice(magic_ball_answers))
    else:
        # Просим пользователя задать вопрос
        bot.send_message(message.chat.id, 'Не понимаю о чем ты... Просто задай вопрос')
    # Сбрасываем состояние пользователя
    set_user_state(message, True)
@bot.message_handler(func=lambda message: not get_user_state(message))
def handle_text(message):
    # Если состояние пользователя не позволяет использовать кнопки, отправляем сообщение
    bot.send_message(message.chat.id, 'Пожалуйста, нажми на кнопку "старт", чтобы использовать бота.')
# Обработчик текстовых сообщений для кнопки 'Викторина'
@bot.message_handler(func=lambda message: get_user_state(message) and message.text == 'Викторина')
def handle_quiz_button(message):
    question_num = random.choice(list(quiz_questions.keys()))
    current_questions[message.chat.id] = question_num
    send_quiz_question(message, question_num)

# Функция для отправки вопроса викторины
def send_quiz_question(message, question_num):
    question_data = quiz_questions[question_num]
    bot.send_message(message.chat.id, question_data['question'])
    set_user_state(message, 'Викторина_Ожидание_Ответа')

# Обработчик текстовых сообщений для ответов на викторину
@bot.message_handler(func=lambda message: get_user_state(message) == 'Викторина_Ожидание_Ответа')
def handle_quiz_answer(message):
    question_num = current_questions.get(message.chat.id)
    if question_num is not None:
        correct_answer = quiz_questions[question_num]['correct']
        if message.text.strip().lower() == correct_answer.lower():
            bot.send_message(message.chat.id, 'Правильно! Переходим к следующему вопросу... 👍')
            # Выбираем следующий вопрос
            next_question_num = random.choice(list(quiz_questions.keys()))
            while next_question_num == question_num:  # Убедимся, что вопрос не повторяется
                next_question_num = random.choice(list(quiz_questions.keys()))
            current_questions[message.chat.id] = next_question_num
            send_quiz_question(message, next_question_num)
        else:
            bot.send_message(message.chat.id, 'Неправильно. Викторина окончена. 😢')
            set_user_state(message, True)
            del current_questions[message.chat.id]
# Функция для отправки анекдотов
def send_anecdote(message):
    index = random.randint(0, len(anecdotes) - 1)
    bot.send_message(message.chat.id, anecdotes[index])
    set_user_state(message, 'Анекдоты')

# Обработчик текстовых сообщений для кнопки 'Анекдоты'
@bot.message_handler(func=lambda message: get_user_state(message) and message.text == 'Анекдоты')
def handle_anecdotes_button(message):
    send_anecdote(message)

# Обработчик текстовых сообщений для получения следующего анекдота
@bot.message_handler(func=lambda message: get_user_state(message) == 'Анекдоты')
def handle_next_anecdote(message):
    if message.text.lower() == 'еще':
        send_anecdote(message)
    else:
        bot.send_message(message.chat.id, 'Не понимаю. Если хочешь услышать еще анекдот, напишите "еще".')
        set_user_state(message, True)
# Добавляем список фактов
facts = [
    'Самое большое животное на планете - синий кит.',
    'Вода составляет около 60% веса человеческого тела.',
    'Мед - единственный продукт питания, который не портится.',
    'Самое маленькое млекопитающее в мире - бамбуковый летучий лемур.',
    'Около 70% кислорода на Земле производится океанами.',
    'Кофеин - самый популярный психоактивный компонент в мире.',
    'Бананы - это ягоды, а клубника - нет.',
    'Самое длинное слово в русском языке содержит 35 букв - "электрофотополупроводниковый".',
    'Венера - единственная планета в Солнечной системе, которая вращается вокруг своей оси в обратном направлении.',
    'Самое глубокое место в океане - Марианская впадина, её глубина превышает 11 километров.'
]
# Функция для отправки фактов
def send_fact(message):
    index = random.randint(0, len(facts) - 1)
    bot.send_message(message.chat.id, facts[index])
    set_user_state(message, 'Факты')

# Обработчик текстовых сообщений для кнопки 'Факты'
@bot.message_handler(func=lambda message: get_user_state(message) and message.text == 'Факты')
def handle_facts_button(message):
    send_fact(message)

# Обработчик текстовых сообщений для получения следующего факта
@bot.message_handler(func=lambda message: get_user_state(message) == 'Факты')
def handle_next_fact(message):
    if message.text.lower() == 'еще':
        send_fact(message)
    else:
        bot.send_message(message.chat.id, 'Не понимаю. Если хочешь узнать еще факт, напишите "еще".')
        set_user_state(message, True)


bot.polling(none_stop=True)
