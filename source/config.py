class DatabaseConfig(object):
    def __init__(self, status, name, user, password, host, port=5432, tables=None):
        self.status = status
        self.name = name
        self.user = user
        self.password = password
        self.port = port
        self.host = host
        self.tables = tables
    
    def __repr__(self):
        print('Status: {}'.format(self.status))
        print('Name: {}'.format(self.name))
        print('User: {}'.format(self.user))
        print('Password: -hidden-')
        print('Port: {}'.format(self.port))
        print('Tables: {}'.format(str(self.tables)))