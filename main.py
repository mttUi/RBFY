import telebot
from telebot import types
import pandas as pd

bot = telebot.TeleBot("7221264332:AAGeFT7XSjgEkOtgGhJJ2wXKEG-0FSNF4ow")


# Функция для чтения расписания из Excel файла
def get_schedule(sheet_name, day):
    try:
        # Загрузите Excel файл
        df = pd.read_excel('schedule.xlsx', sheet_name=sheet_name, engine='openpyxl', index_col=0)

        # Преобразуем расписание для конкретного дня в текстовый формат
        schedule_text = f"Расписание для {day}:\n\n"
        for index, row in df.iterrows():
            schedule_text += f"{index}: {row[day]}\n"
        return schedule_text
    except Exception as e:
        return f"Ошибка при чтении расписания для {sheet_name} и {day}: {e}"


# Словарь для хранения данных о пользователе
user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌐Расписание")
    btn2 = types.KeyboardButton("👤Информация")
    markup.add(btn1, btn2)

    pbtn = types.InlineKeyboardMarkup()
    pbtn1 = types.InlineKeyboardButton(text='РБД/1гр/1пг', callback_data='РБД 1гр 1пг')
    pbtn2 = types.InlineKeyboardButton(text='РБД/1гр/2пг', callback_data='РБД 1гр 2пг')
    pbtn3 = types.InlineKeyboardButton(text='РБД/2гр/1пг', callback_data='РБД 2гр 1пг')
    pbtn4 = types.InlineKeyboardButton(text='РБД/2гр/2пг', callback_data='РБД 2гр 2пг')
    pbtn5 = types.InlineKeyboardButton(text='РИСКУ/1гр/1пг', callback_data='РИСКУ 1гр 1пг')
    pbtn6 = types.InlineKeyboardButton(text='РИСКУ/1гр/2пг', callback_data='РИСКУ 1гр 2пг')
    pbtn.add(pbtn1, pbtn2, pbtn3, pbtn4, pbtn5, pbtn6)

    sent_message = bot.send_message(message.chat.id, "Выберите свою группу обучения", reply_markup=pbtn,
                                    parse_mode='html')

    # Сохранение данных о пользователе
    user_data[message.chat.id] = {'last_bot_message_ids': [sent_message.message_id]}

    # Удаление сообщения пользователя
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if ' ' in call.data:
        # Сохраняем выбранную группу и предлагаем выбрать день недели
        user_data[call.message.chat.id]['group'] = call.data
        send_day_selection(call.message)
    elif call.data == 'back':
        # Возвращаем пользователя к выбору дня недели
        send_day_selection(call.message)
    elif call.data == 'select_group':
        # Возвращаем пользователя к выбору группы
        start(call.message)
    else:
        # Обработка выбора дня недели и отправка расписания
        try:
            group = user_data[call.message.chat.id].get('group')
            if group:
                schedule_text = get_schedule(group, call.data)
                schedule_text += "\n\nВыберите действие:"
                schedule_markup = types.InlineKeyboardMarkup()
                back_button = types.InlineKeyboardButton(text="Назад", callback_data='back')
                select_group_button = types.InlineKeyboardButton(text="К выбору группы", callback_data='select_group')
                schedule_markup.add(back_button, select_group_button)
                sent_message = bot.send_message(call.message.chat.id, schedule_text, reply_markup=schedule_markup)

                # Удаление предыдущих сообщений бота
                delete_previous_messages(call.message.chat.id)
                user_data[call.message.chat.id]['last_bot_message_ids'] = [sent_message.message_id]

            else:
                sent_message = bot.send_message(call.message.chat.id, "Ошибка: сначала выберите группу.")
                delete_previous_messages(call.message.chat.id)
                user_data[call.message.chat.id]['last_bot_message_ids'] = [sent_message.message_id]

        except Exception as e:
            sent_message = bot.send_message(call.message.chat.id, f"Ошибка при обработке запроса: {e}")
            delete_previous_messages(call.message.chat.id)
            user_data[call.message.chat.id]['last_bot_message_ids'] = [sent_message.message_id]


@bot.message_handler(content_types=['text'])
def otvet(message):
    if message.text == "👤Информация":
        sent_message = bot.send_message(message.chat.id, "Создатели тутуттутут")

        # Удаление сообщений пользователя и бота
        delete_previous_messages(message.chat.id)
        user_data[message.chat.id] = {'last_bot_message_ids': [sent_message.message_id]}

        # Удаление сообщения пользователя
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def send_day_selection(message):
    days_markup = types.InlineKeyboardMarkup()
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for day in days:
        days_markup.add(types.InlineKeyboardButton(text=day, callback_data=day))
    sent_message = bot.send_message(message.chat.id, "Выберите день недели:", reply_markup=days_markup)

    # Удаление предыдущих сообщений бота
    delete_previous_messages(message.chat.id)
    user_data[message.chat.id]['last_bot_message_ids'] = [sent_message.message_id]


def delete_previous_messages(chat_id):
    if chat_id in user_data:
        for message_id in user_data[chat_id].get('last_bot_message_ids', []):
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id} в чате {chat_id}: {e}")


bot.polling(none_stop=True)
