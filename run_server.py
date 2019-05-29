from flask import Flask
from flask import request
import pars
import telebot
import os


token = os.environ.get('TOKEN')
app_name = os.environ.get('APP_NAME')
bot = telebot.TeleBot(token, threaded=False)

server = Flask(__name__)


#Головна кнопка
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('В ТЯЗІВ  ✈️')


# Inline нопка "налаштування"
keyboard3 = telebot.types.InlineKeyboardMarkup()
call_b = telebot.types.InlineKeyboardButton(text='Налаштування', callback_data='Налаштування')
keyboard3.add(call_b)


# Клавіатура для вибору кількості автобусів
keyboard2 = telebot.types.InlineKeyboardMarkup()
for i in range(1,6):
    cal_but = telebot.types.InlineKeyboardButton(text=str(i), callback_data=str(i))
    keyboard2.add(cal_but)


# Реакція на команду '/start'
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text='Привіт, ' + message.from_user.first_name + '. ' + 'Щоб отримати розклад автобусів натисніть кнопку ⬇️', reply_markup=keyboard)


# Реакція на команду '/help'
@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text='Бот показує розклад автобусів найближчих по часу відправлення в Тязів. Для початку роботи натисніть /start')


# Обробка отриманого повідомлення
@bot.message_handler(func=lambda message: True, content_types=[ 'text','sticker', 'audio', 'video', 'photo', 'document', 'video_note', 'voice', 'location', 'contact'])
def send_shedule(message):
    if message.text is not None:

        if '✈️' in message.text:
            pars.get_number_bus(message.chat.id)
            bot.send_message(chat_id=message.chat.id, text='*'+pars.shedule()+'*', reply_markup=keyboard3, parse_mode='Markdown')

        else:
            bot.send_sticker(chat_id=message.chat.id, data='CAADAgAD5QEAAnELQgVO8tCPFPdaDgI')

    else:
        bot.send_sticker(chat_id=message.chat.id, data = 'CAADAgAD5QEAAnELQgVO8tCPFPdaDgI') # Якщо отримане повідомлення не правильне - відсилаємо стікер


# Обробка отриманих даних з Inline клавіатури
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    if call.data == 'Налаштування':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Виберіть скільки автобусів показувати:', reply_markup=keyboard2)

    elif int(call.data) in range(1,6):
        # Відправка числа  для задання кількості відображених автобусів
        pars.number_bus(call.data, call.message.chat.id)
        pars.get_number_bus(call.message.chat.id)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*" + pars.shedule() +'*', parse_mode='Markdown', reply_markup=keyboard3)


# Обробка POST запиту
@server.route('/' + token, methods=['POST'])
def get_message():
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
        return '!', 200


# Обробка GET запиту
@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(app_name, token))
    return "Hello from Heroku! Bot is working", 200


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
