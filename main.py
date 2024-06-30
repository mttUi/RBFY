import telebot
from telebot import types
import random

bot = telebot.TeleBot("7221264332:AAGeFT7XSjgEkOtgGhJJ2wXKEG-0FSNF4ow")

image_list = [
    r'C:\Users\ASUS\Documents\GitHub\RBFY\capcha\image1.jpg',
    r'C:\Users\ASUS\Documents\GitHub\RBFY\capcha\image2.png',
    r'C:C:\Users\ASUS\Documents\GitHub\RBFY\capcha\image3.gif'
]

last_message_id = None
chat_id_group = -1002205901677
message_thread_id = 2

@bot.message_handler(commands=['start'])
def capcha(message):
    global last_message_id
    global chat_id_group
    if last_message_id:
        bot.delete_message(message.chat.id, last_message_id)
    bot.delete_message(message.chat.id, message.message_id)

    image_path = random.choice(image_list)
    caption_text = ("Здравствуйте! Это бот, который поможет узнать вам расписание ваших пар📝\n\n"
                    "🇷🇺 RUS:\nДля начала работы с ботом решите капчу:\n\n"
                    "🇺🇸 ENG:\nTo start working with the bot, solve the captcha:\n\n")
    with open(image_path, 'rb') as photo:
        sent_message = bot.send_photo(message.chat.id, photo=photo, caption=caption_text, parse_mode='html')
        last_message_id = sent_message.message_id

    chat_id_group = message.chat.id  # Сохраняем идентификатор группы


@bot.message_handler(content_types=['text'])
def otvet(message):
    global last_message_id
    global chat_id_group
    if last_message_id:
        bot.delete_message(message.chat.id, last_message_id)
    bot.delete_message(message.chat.id, message.message_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌐Расписание")
    btn2 = types.KeyboardButton("👤Информация")
    markup.add(btn1, btn2)

    pbtn = types.InlineKeyboardMarkup()
    pbtn1 = types.InlineKeyboardButton(text='РБД/1гр/1пг', callback_data='1')
    pbtn2 = types.InlineKeyboardButton(text='РБД/1гр/2пг', callback_data='2')
    pbtn3 = types.InlineKeyboardButton(text='РБД/2гр/1пг', callback_data='3')
    pbtn4 = types.InlineKeyboardButton(text='РБД/2гр/2пг', callback_data='4')
    pbtn5 = types.InlineKeyboardButton(text='РИСКУ/1гр/1пг', callback_data='5')
    pbtn6 = types.InlineKeyboardButton(text='РИСКУ/1гр/2пг', callback_data='6')
    pbtn.add(pbtn1, pbtn2, pbtn3, pbtn4, pbtn5, pbtn6)


    if message.text in ['76447', '2VYK', 'W6 8HP']:
        sent_message = bot.send_message(message.chat.id,
                                        "🇷🇺 RUS:\n✅ Капча решена верно. Можете спокойно пользоваться ботом.\n"
                                        "Если у вас не появилось меню, то напишите :menu\n"
                                        "🇺🇸 ENG:\n✅ The captcha is solved correctly.\n"
                                        "You can safely use the bot.\n"
                                        "If you don't have a menu, then write :menu",
                                        reply_markup=markup, parse_mode='html')
        last_message_id = sent_message.message_id
    if message.text == "🌐Расписание":
        sent_message = bot.send_message(message.chat.id,"Выберите свою группу обучения", reply_markup=pbtn,parse_mode='html')
        last_message_id = sent_message.message_id




bot.polling(none_stop=True)
