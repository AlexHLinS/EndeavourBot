import os

import telebot


import messageparcer
import dbworker


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
                    f'[+] Token {self.getToken()} loaded from file {token_file}')
        except FileNotFoundError:
            if self.__is_log_needed:
                print(f'[!] Token can\'t load from file {token_file}')
            try:
                self.setToken(os.environ['key_1'])
                if self.__is_log_needed:
                    print(
                        f'[+] Token {self.getToken()} loaded from system variable key_1')
            except:
                return None


class hlinsBot:
    __token = None
    __bot = None
    __bot_url = ''

    def setToken(self, token_string):
        self.__token = token_string

    def getToken(self):
        return self.__token

    def __init__(self, token_string, database: dbworker.postgresSQLBotDB):
        self.database = database
        self.setToken(token_string)
        __bot = telebot.AsyncTeleBot(token=self.getToken())
        #server = Flask(__name__)

        @__bot.message_handler(func=lambda m: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                                   'text', 'location', 'contact', 'sticker'])
        def receivedMessage(message):
            self.parseMessage(__bot, message, self.database)
            pass

        try:
            __bot.polling()
        except:
            print('[Bot panic!]Restarting!')
            os.execlp('python',os.cwd+'/main.py')

    def parseMessage(self, bot, message, database):
        #bot.reply_to(message, 'Under construction')
        parcer = messageparcer.messageparcer(message, bot, database)
        print(
            f"[>]recived {message.content_type} from \"{message.from_user.username}\"[id:{message.from_user.id}] ")
