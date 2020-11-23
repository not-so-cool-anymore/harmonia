from typing import List

class DatabaseConfig(object):
    status: str
    name: str
    user: str
    password: str
    port: int
    host: str

    def __init__(self, status, name, user, password, host, port=5432):
        self.status = status
        self.name = name
        self.user = user
        self.password = password
        self.port = port
        self.host = host
    
    def __repr__(self):
        print('Status: {}'.format(self.status))
        print('Name: {}'.format(self.name))
        print('User: {}'.format(self.user))
        print('Password: -hidden-')
        print('Port: {}'.format(self.port))
        print('Host: {}'.format(self.host))
    
        return ""