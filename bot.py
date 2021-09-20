import os

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
                print(
                    f"[+] Token {self.getToken()} loaded from file {token_file}")
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

        __bot.polling()

    def parseMessage(self, bot, message):
        #bot.reply_to(message, 'Under construction')
        parcer = messageparcer.messageparcer(message, bot)
        
        
        
