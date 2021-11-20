import sys
from bot import botToken, hlinsBot

TOKEN_FILE_NAME ='bot.token'



def main():

    tkn = botToken(TOKEN_FILE_NAME)
    print(tkn.getToken())
    bot = hlinsBot(tkn.getToken())
    return 0

if __name__ == '__main__':
    main()