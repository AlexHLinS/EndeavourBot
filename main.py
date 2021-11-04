import sys
import os
from flask import Flask, request
from bot import botToken, hlinsBot
import telebot

TOKEN_FILE_NAME ='bot.token'
TOKEN = botToken(TOKEN_FILE_NAME).getToken()

bot_server = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(unc=lambda m: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                                   'text', 'location', 'contact', 'sticker'])
def reply_to_message(message):
    bot.send_message(message.chat.id, message.text)


@bot_server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@bot_server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('key_2', 'https://hsetelebot.herokuapp.com/') + TOKEN) #
    return "!", 200




if __name__ == '__main__':
    host = "0.0.0.0"
    port=int(os.environ.get('key_3', 5001))
    bot_server.run(host=host, port=port)