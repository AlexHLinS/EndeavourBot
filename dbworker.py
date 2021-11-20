import json

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
        with open(filename) as f:
            dump = json.load(f)
            self.setHost(dump['host'])
            self.setPort(dump['port'])
            self.setUsername(dump['username'])
            self.setPassword(dump['password'])
            self.setDatabase(dump['database'])

def main():
    psqlcinf = postgresSQLconnectionInfo('db.token')
    
    return 0


if __name__ == "__main__":
    main()
