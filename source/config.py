class DatabaseConfig(object):
    def __init__(self, status, name, user, password, tables):
        self.status = status
        self.name = name
        self.user = user
        self.password = password
        self.tables = tables