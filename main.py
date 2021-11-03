import sys
import os
from flask import Flask, request
from bot import botToken, hlinsBot
import telebot

TOKEN_FILE_NAME ='bot.token'
TOKEN = 'unsetted'
bot_server = Flask(__name__)
bot = telebot.AsyncTeleBot(TOKEN)


@bot_server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@bot_server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('key_2', 'https://hsetelebot.herokuapp.com/') + TOKEN) #
    return "!", 200

@bot.message_handler(unc=lambda m: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                                   'text', 'location', 'contact', 'sticker'])
def reply_to_message(message):
    bot.parseMessage(bot,message)


if __name__ == '__main__':
    host = "0.0.0.0"
    port=int(os.environ.get('key_3', 5001))
    tkn = botToken(TOKEN_FILE_NAME)
    TOKEN = tkn.getToken()
    bot = hlinsBot(TOKEN)
    print(TOKEN)
    bot_server.run(host=host, port=port)