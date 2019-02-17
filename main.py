# encoding: utf-8
import telebot
from parser import parse
from circular_buffer import Circular_Buffer

bot = telebot.TeleBot('742661651:AAFMQWZo7kzLJV9F9jegq_NFEarnwE2mNq4')
clients = []
buf = None

def send_task(client):
    if client.get_text() == 'aqua':
        bot.send_photo(client.chat_id, open('src/img/aqua1.jpg', 'rb').read())
        bot.send_photo(client.chat_id, open('src/img/aqua2.jpg', 'rb').read())
    elif client.get_type() == 'img':
        bot.send_photo(client.chat_id, client.get_text())
    elif client.get_type() == 'audio':
        bot.send_audio(client.chat_id, client.get_text())
    elif client.get_type() == 'video':
        bot.send_video(client.chat_id, client.get_text())
    else:
        bot.send_message(client.chat_id, client.get_text())

def client_exists(chat_id):
    for client in clients:
        if client.chat_id == chat_id:
            return client
    return False
     
@bot.message_handler(commands=['start'])
def start(message):
    if client_exists(message.chat.id):
        bot.reply_to(message, "Вы уже зарегистрировались")
    else:
        client = buf.create_client(message.chat.id)
        clients.append(client)
        send_task(client)

@bot.message_handler(commands=['help'])
def help(message):
    client = client_exists(message.chat.id)
    if client:
        if client.get_help():
            bot.reply_to(message, "Внимание, помощью вы сможете воспользоваться только один раз!!!\nЧтобы получить помощь отправьте \n/help второй раз")
        else:
            bot.reply_to(message, "Нужна помощь? Обратитесь к вожатым))0)0)")

@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith('/'))
def main(message):
    client = client_exists(message.chat.id)
    if client:
        # None - команда уже закончила квест, True - ответ правильный, False - ответ неправильный
        answer = client.answer(message.text[1:])
        if isinstance(answer, type(None)):
            bot.reply_to(message, "Вы закончили квест! Поздравляем")
        elif answer == True:
            print(client.chat_id, client.passed)
            send_task(client)
        else:
            bot.reply_to(message, "Это неправильный ответ")
    else:
        bot.reply_to(message, "Вы не зарегистрировались. Отправьте /start")

@bot.message_handler(func=lambda msg: msg.text and not msg.text.startswith('/'))
def no_functions(message):
    bot.reply_to(message, "Если вы хотели отправить ответ, нужно было на писать так\n\"/{}\"".format(message.text))


if __name__ == "__main__":
    arr = parse('config')
    buf = Circular_Buffer(arr)
    while True:
        try:
            bot.polling()
        except Error as e:
            print("lolkek")
            pass


    
