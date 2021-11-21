import sys
from bot import botToken, hlinsBot
from dbworker import postgresSQLconnectionInfo, postgresSQLBotDB

TOKEN_FILE_NAME = 'bot.token'


def main():
    psqlcinf = postgresSQLconnectionInfo('db.token')
    db = postgresSQLBotDB(psqlcinf)
    tkn = botToken(TOKEN_FILE_NAME)
    print(tkn.getToken())
    bot = hlinsBot(tkn.getToken(), db)
    return 0


if __name__ == '__main__':
    main()
