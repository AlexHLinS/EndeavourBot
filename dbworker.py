import json
import psycopg2
from psycopg2 import sql


class postgresSQLconnectionInfo:

    def setHost(self, host):
        self.host = host

    def getHost(self):
        return self.host

    def setPort(self, port):
        self.port = port

    def getPort(self):
        return self.port

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username

    def setPassword(self, password):
        self.password = password

    def getPassword(self):
        return self.password

    def setDatabase(self, database):
        self.database = database

    def getDatabase(self):
        return self.database

    def __init__(self, filename):
        ''' PostgresSQL base connection info object load and store \
            connection data from \'filename\' file
        '''
        with open(filename) as f:
            dump = json.load(f)
            self.setHost(dump['host'])
            self.setPort(dump['port'])
            self.setUsername(dump['username'])
            self.setPassword(dump['password'])
            self.setDatabase(dump['database'])


class postgresSQLBotDB:
    def __init__(self, connection_info):
        ''' Create a postgresSQL base interface from a connection info
            \nWhere connection_info is postgresSQLconnectionInfo object
        '''
        self.dbname = connection_info.getDatabase()
        self.user = connection_info.getUsername()
        self.password = connection_info.getPassword()
        self.host = connection_info.getHost()
        self.conn = psycopg2.connect(dbname=self.dbname,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host)

    def sendRequest(self, sql_request_string):
        ''' Execute SQL Request
            Params:
            - sql_request_string - SQL Request string (str)
            Returns:
            - False if request Unsuccesfull
            - Result of request if successful and request have to return data
            - True if request successful 
        '''
        with self.conn.cursor() as cursor:
            self.conn.autocommit = True
            sql_request = psycopg2.sql.SQL(sql_request_string)
            try:
                cursor.execute(sql_request)
                try:
                    result = cursor.fetchall()
                except Exception:
                    result = True
            except Exception:
                return False
            return result

    def isUserExist(self, user_id):
        ''' Check the user id existing in dbase
            Returns:
            - True if User ID exist in base
            - False if does not exist
        '''
        req_string = f"SELECT alias_name FROM users WHERE telegram_user_id=\'{user_id}\'"
        res = self.sendRequest(req_string)
        if  res in [False, None] or len(res) < 1:
            return False
        return True

    def addUser(self, user_id, user_name, alias_name):
        ''' Create a new user in dbase
            \nuser_id - Telegram user ID
            \nuser_name - Telegram user name
            \nalias_name - Custom user name given from his self
            \nReturns:
            \n- True if user added succesfull or update_time field is updates
            \n- False if error occured
        '''
    
        if self.isUserExist(user_id):
            if alias_name != '':    
                req_string = f' UPDATE users \
                                SET update_time=NOW(), \
                                    alias_name=\'{alias_name}\' \
                                WHERE telegram_user_id=\'{user_id}\''
            else:
                req_string = f' UPDATE users \
                                SET update_time=NOW()\
                                WHERE telegram_user_id=\'{user_id}\''
        else:
            req_string = f''' INSERT INTO users 
                                        (telegram_user_id, 
                                        telegram_user_name, 
                                        alias_name, 
                                        create_time, 
                                        update_time) 
                            VALUES (\'{user_id}\',  
                                    \'{user_name}\',  
                                    \'{alias_name}\',  
                                        NOW(), 
                                        NOW())'''
        return self.sendRequest(req_string)

    def isTranscribationResultExist(self, md5hash):
        req_string = f'''   SELECT  content_text
                            FROM    voicetotextresults
                            WHERE   md5sum=\'{md5hash}\''''
        res = self.sendRequest(req_string)
        if  res in [False, None] or len(res) < 1:
            return False
        return True

    def addTranscribationResult(self, md5hash, content_text):
        ''' Adding transcribation result to DB
        '''
        if self.isTranscribationResultExist(md5hash):
            return False
        req_string = f'''   INSERT INTO voicetotextresults 
                                        (md5sum, content_text, create_time)
                            VALUES      (\'{md5hash}\' , \'{content_text}\' , NOW()) '''
        return self.sendRequest(req_string)

    def getTranscribationResult(self, md5hash):
        req_string = f'''   SELECT content_text
                            FROM voicetotextresults
                            WHERE md5sum = \'{md5hash}\''''
        
        return self.sendRequest(req_string)

    def addTranscribationRequest(self, user_id, md5hash, forward_from):
        req_string = f'''  INSERT INTO voicetotextrequests 
                                                (create_time, telegram_user_id, md5sum, forward_from_id)
                           VALUES               (NOW(), 
                                                \'{user_id}\', 
                                                \'{md5hash}\',
                                                \'{forward_from}\') '''
        return self.sendRequest(req_string)

def main():
    psqlcinf = postgresSQLconnectionInfo('db.token')
    db = postgresSQLBotDB(psqlcinf)

    return 0


if __name__ == "__main__":
    main()
