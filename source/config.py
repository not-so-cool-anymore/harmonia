class DatabaseConfig(object):
    def __init__(self, status, name, user, password, tables=None):
        self.status = status
        self.name = name
        self.user = user
        self.password = password
        self.tables = tables
    
    def __repr__(self):
        print('Status: {}'.format(self.status))
        print('Name: {}'.format(self.name))
        print('User: {}'.format(self.user))
        print('Password: -hidden-')
        print('Tables: {}'.format(str(self.tables)))