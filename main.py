import telebot
from telebot import types
import pandas as pd

bot = telebot.TeleBot("7221264332:AAGeFT7XSjgEkOtgGhJJ2wXKEG-0FSNF4ow")


# Функция для чтения расписания из Excel файла
def get_schedule(sheet_name):
    # Загрузите Excel файл
    df = pd.read_excel('schedule.xlsx', sheet_name=sheet_name, engine='openpyxl', index_col=0)

    # Преобразуем расписание в текстовый формат
    schedule_text = ""
    for index, row in df.iterrows():
        schedule_text += f"{index}:\n"
        for day in df.columns:
            schedule_text += f"{day}: {row[day]}\n"
        schedule_text += "\n"
    return schedule_text


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌐Расписание")
    btn2 = types.KeyboardButton("👤Информация")
    markup.add(btn1, btn2)

    pbtn = types.InlineKeyboardMarkup()
    pbtn1 = types.InlineKeyboardButton(text='РБД/1гр/1пг', callback_data='РБД 1гр 1пг')
    pbtn2 = types.InlineKeyboardButton(text='РБД/1гр/2пг', callback_data='РБД/1гр/2пг')
    pbtn3 = types.InlineKeyboardButton(text='РБД/2гр/1пг', callback_data='РБД/2гр/1пг')
    pbtn4 = types.InlineKeyboardButton(text='РБД/2гр/2пг', callback_data='РБД/2гр/2пг')
    pbtn5 = types.InlineKeyboardButton(text='РИСКУ/1гр/1пг', callback_data='РИСКУ/1гр/1пг')
    pbtn6 = types.InlineKeyboardButton(text='РИСКУ/1гр/2пг', callback_data='РИСКУ/1гр/2пг')
    pbtn7 = types.InlineKeyboardButton(text='🌐Информация', callback_data='7')
    pbtn.add(pbtn1, pbtn2, pbtn3, pbtn4, pbtn5, pbtn6, pbtn7)

    sent_message = bot.send_message(message.chat.id, "Выберите свою группу обучения", reply_markup=pbtn,
                                    parse_mode='html')

    # Удаление сообщения пользователя и бота
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    schedule_text = get_schedule(call.data)
    bot.send_message(call.message.chat.id, schedule_text)


@bot.message_handler(content_types=['text'])
def otvet(message):
    pbtn = types.InlineKeyboardMarkup()
    pbtn1 = types.InlineKeyboardButton(text='РБД/1гр/1пг', callback_data='РБД 1гр 1пг')
    pbtn2 = types.InlineKeyboardButton(text='РБД/1гр/2пг', callback_data='РБД/1гр/2пг')
    pbtn3 = types.InlineKeyboardButton(text='РБД/2гр/1пг', callback_data='РБД/2гр/1пг')
    pbtn4 = types.InlineKeyboardButton(text='РБД/2гр/2пг', callback_data='РБД/2гр/2пг')
    pbtn5 = types.InlineKeyboardButton(text='РИСКУ/1гр/1пг', callback_data='РИСКУ/1гр/1пг')
    pbtn6 = types.InlineKeyboardButton(text='РИСКУ/1гр/2пг', callback_data='РИСКУ/1гр/2пг')
    pbtn7 = types.InlineKeyboardButton(text='🌐Информация', callback_data='7')
    pbtn.add(pbtn1, pbtn2, pbtn3, pbtn4, pbtn5, pbtn6, pbtn7)

    if message.text == "🌐Информация":
        sent_message = bot.send_message(message.chat.id, "Создатели тутуттутут", reply_markup=pbtn, parse_mode='html')

        # Удаление сообщения пользователя и бота
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


bot.polling(none_stop=True)
