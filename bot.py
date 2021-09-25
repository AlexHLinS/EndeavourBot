import os
from aiohttp import web

import telebot

import messageparcer


class botToken:
    __token_string = ''
    __is_log_needed = False

    def setToken(self, token_string):
        self.__token_string = token_string

    def getToken(self):
        return self.__token_string

    def __init__(self, token_file):
        try:
            file = open(token_file, 'r')
            self.setToken(file.readline())
            if self.__is_log_needed:
                print(f"[+] Token {self.getToken()} loaded from file {token_file}")
        except FileNotFoundError:
            if self.__is_log_needed:
                print(f"[!] Token can't load from file {token_file}")
            try:
                self.setToken(os.environ['key_1'])
                if self.__is_log_needed:
                    print(
                        f"[+] Token {self.getToken()} loaded from system variable key_1")
            except:
                return None


class hlinsBot:
    __token = None
    __bot = None

    def setToken(self, token_string):
        self.__token = token_string

    def getToken(self):
        return self.__token

    def __init__(self, token_string):
        self.setToken(token_string)
        __bot = telebot.AsyncTeleBot(token=self.getToken())

        @__bot.message_handler(func=lambda m: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                                   'text', 'location', 'contact', 'sticker'])
        def receivedMessage(message):
            self.parseMessage(__bot, message)
            pass
        # TODO: change to webhook here
        #try:
        print('starting webhook method ... ')
        web_hook_url = os.environ['key_2']+self.getToken()
        print(f'web_hook_url = os.environ[key_2]+self.getToken() - ok!')
        web_hook_port = int(os.environ['key_3'])
        print(f'web_hook_port = int(os.environ[key_3]) - ok!')
        __bot.remove_webhook()
        print('__bot.remsove_webhook() - ok!')
        __bot.set_webhook(url = web_hook_url)
        print('__bot.set_webhook(url = web_hook_url) - ok!')
        app = web.Application()
        print('app = web.Application() - ok!')
        web.run_app(app, host=os.environ['key_5'], port=web_hook_port, url_path = self.getToken())
        print(f'web.run_app(app, host=os.environ[key_5], port=web_hook_port, url_path = self.getToken()) - ok!')
        print(f'Succes! Webhook method started at {web_hook_url}:{web_hook_port}!')
        
        '''except Exception:
            print('Unsuccesfull try of set_webhook method, using pooling method')
            __bot.polling()'''

    def parseMessage(self, bot, message):
        #bot.reply_to(message, 'Under construction')
        parcer = messageparcer.messageparcer(message, bot)
        print(f"[>]recived {message.content_type} from \"{message.from_user.username}\"[id:{message.from_user.id}] ")
        
        
        
