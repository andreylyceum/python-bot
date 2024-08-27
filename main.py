import telebot
import sqlite3
import datetime
from data.teory_messages import THEORY_MSGS
from data.practice_messages import PRACTICE_MSGS
from images.token import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
number = 0
user_message = ""


@bot.message_handler(commands=["start"])
def start(message):
    conn = sqlite3.connect("python_bot_sql")
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            telegram_id TEXT,
            timestamp TEXT
        )"""
    )
    conn.commit()
    name = message.from_user.first_name
    telegram_id = message.from_user.username
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    cur.execute("INSERT INTO users (name, telegram_id, timestamp) VALUES (?, ?, ?)",
                (name, telegram_id, timestamp))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, THEORY_MSGS["greeting text"])


@bot.message_handler(commands=["learn"])
def first_message(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("теория", callback_data="теория")
    btn2 = telebot.types.InlineKeyboardButton("практика", callback_data="практика")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "теория":
        theory(call.message)
    elif call.data == "практика":
        practice(call.message)
    elif call.data == "основные понятия":
        theory_basic_topics(call.message)
    elif call.data == "циклы":
        theory_for_topics(call.message)
    elif call.data == "коллекции":
        theory_collections_topics(call.message)
    elif call.data == "функции":
        theory_func_topics(call.message)
    elif call.data == "ввод stdin":
        theory_stdin_topics(call.message)
    elif call.data == "библиотеки":
        theory_books_topics(call.message)
    elif call.data == "ООП":
        theory_oop_topics(call.message)
    elif (
         call.data == "циклы_" or
         call.data == "коллекции_" or
         call.data == "функции_" or
         call.data == "потоковый ввод_" or
         call.data == "библиотеки_" or
         call.data == "ООП_"
    ):
        global user_message
        user_message = call.data
        bot.send_message(call.message.chat.id, PRACTICE_MSGS[user_message])
        bot.register_next_step_handler(call.message, number_of_task)
    else:
        bot.send_message(call.message.chat.id, THEORY_MSGS[call.data], parse_mode="Markdown")


def theory(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("основные понятия", callback_data="основные понятия")
    btn2 = telebot.types.InlineKeyboardButton("циклы", callback_data="циклы")
    btn3 = telebot.types.InlineKeyboardButton("коллекции", callback_data="коллекции")
    btn4 = telebot.types.InlineKeyboardButton("функции", callback_data="функции")
    btn5 = telebot.types.InlineKeyboardButton("ввод stdin", callback_data="ввод stdin")
    btn7 = telebot.types.InlineKeyboardButton("библиотеки", callback_data="библиотеки")
    btn8 = telebot.types.InlineKeyboardButton("ООП", callback_data="ООП")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn7, btn8)
    bot.send_message(message.chat.id, "Выберите раздел с теорией", reply_markup=markup)


def theory_basic_topics(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    btn1 = telebot.types.InlineKeyboardButton("встроенные функции", callback_data="встроенные функции")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)


def theory_for_topics(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("цикл for", callback_data="цикл for")
    btn2 = telebot.types.InlineKeyboardButton("цикл while", callback_data="цикл while")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)


def theory_collections_topics(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("методы списков", callback_data="методы списков")
    markup.row(btn1)
    btn2 = telebot.types.InlineKeyboardButton("методы строк", callback_data="методы строк")
    btn3 = telebot.types.InlineKeyboardButton("словари", callback_data="словари")
    markup.row(btn2, btn3)
    btn4 = telebot.types.InlineKeyboardButton("множества", callback_data="множества")
    btn5 = telebot.types.InlineKeyboardButton("кортежи", callback_data="кортежи")
    markup.row(btn4, btn5)
    bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)


def theory_func_topics(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("декораторы", callback_data="декораторы")
    btn4 = telebot.types.InlineKeyboardButton("map, sorted, filter", callback_data="map, sorted, filter")
    markup.row(btn4, btn1)
    btn2 = telebot.types.InlineKeyboardButton("лямбда-функции", callback_data="лямбда-функции")
    btn3 = telebot.types.InlineKeyboardButton("рекурсия", callback_data="рекурсия")
    markup.add(btn2, btn3)
    bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)


def theory_stdin_topics(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("потоковый ввод stdin", callback_data="потоковый ввод stdin")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)


def theory_books_topics(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("datetime", callback_data="datetime")
    btn2 = telebot.types.InlineKeyboardButton("random", callback_data="random")
    btn3 = telebot.types.InlineKeyboardButton("numpy", callback_data="numpy")
    btn4 = telebot.types.InlineKeyboardButton("pillow", callback_data="pillow")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)


def theory_oop_topics(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("полиморфизм", callback_data="полиморфизм")
    markup.row(btn1)
    btn2 = telebot.types.InlineKeyboardButton("наследование", callback_data="наследование")
    btn3 = telebot.types.InlineKeyboardButton("инкапсуляция", callback_data="инкапсуляция")
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)


def practice(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("циклы", callback_data="циклы_")
    btn2 = telebot.types.InlineKeyboardButton("коллекции", callback_data="коллекции_")
    btn3 = telebot.types.InlineKeyboardButton("функции", callback_data="функции_")
    btn4 = telebot.types.InlineKeyboardButton("библиотеки", callback_data="библиотеки_")
    btn5 = telebot.types.InlineKeyboardButton("ввод stdin", callback_data="потоковый ввод_")
    btn7 = telebot.types.InlineKeyboardButton("ООП", callback_data="ООП_")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn7)
    bot.send_message(message.chat.id, "Выберите раздел для практики", reply_markup=markup)


def number_of_task(message):
    global number
    global user_message
    try:
        number = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Wrong type, please enter the number of task")
        bot.register_next_step_handler(message, number_of_task)
        return
    if 0 < number < 10:
        file = open(f"images/{user_message}/{number}.png", "rb")
        bot.send_photo(message.chat.id, file)


bot.infinity_polling()

