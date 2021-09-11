import telebot
#from boto.s3.connection import S3Connection
import os
class botToken:
    __token_string = ''
    
    def setToken(self, token_string):
       self.__token_string = token_string
       
    def getToken(self):
        return self.__token_string
    
    def __init__(self, token_file):
        try:
            file = open(token_file, 'r')
            self.setToken(file.readline())
            print(f"[+] Token {self.getToken()} loaded from file {token_file}")
        except FileNotFoundError:
            print(f"[!] Token can't load from file {token_file}")
            self.setToken(os.environ['key_1'])
            print(f"[+] Token {self.getToken()} loaded from system variable key_1")
            
         


class hlinsBot:
    __token = None
    __bot = None
    
    def setToken(self, token_string):
        self.__token = token_string
    
    
    def getToken(self):
        return self.__token
    
    def __init__(self, token_string):
      self.setToken(token_string)
      __bot = telebot.AsyncTeleBot(token = self.getToken())
      
      @__bot.message_handler(func=lambda m: True)
      def receivedMessage(message):
          self.parseMessage(__bot, message)
          pass
      
      __bot.polling()
      
    def parseMessage(self, bot, message):
        bot.reply_to(message, 'Under construction')