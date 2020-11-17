import sys
import json
import psycopg2
import config 
class Syncronizator():
    def __init__(self):
        super().__init__()
    
    def load_config(self, config_file_path):
        try:
            with open(config_file_path, 'r') as config_file:
                config_file_content = config_file.read()

                database_configs = json.loads(config_file_content) 

                self.__main_database_configuration = config.DatabaseConfig(**database_configs[0])
                self.__follower_database_configuration = config.DatabaseConfig(**database_configs[1])
                
            return True
        except Exception as exception:
            print('!!> An exception ocurred:')
            print('!!> \"{}\"'.format(exception))

            return False
    
    def synchronize(self):
        print('>>> Establishing connection to main database')
        main_db_connection, main_db_cursor = self.connect_to_host(self.__main_database_configuration)
        
        if main_db_connection == None or main_db_cursor == None:
            return False
        
        print('>>> Establishing connection to connection database')
        follower_db_connection, follower_db_cursor = self.connect_to_host(self.__follower_database_configuration)

        if follower_db_connection == None or follower_db_cursor == None:
            return False

        for table in self.__main_database_configuration.tables:
            scan_full_table(table)

        return True

    def scan_full_table(self, connection_cursor, table_name):        
        select_query = 'SELECT * FROM {}'.format(table_name)
        connection_cursor.execute(select_query)

        dump_file = open('{}_dump.sql'.format(table_name), 'w')
        
        for row in connection_cursor:
            dump_file.write('INSET INTO {} VALUES ({});'.format(table_name, str(row)))
            print('>>> {}'.format(str(row)))
        
        dump_file.close()
    
    def connect_to_host(self, database_config):
        try:
            connection = psycopg2.connect(
                database = database_config.name,
                user = database_config.user,
                password = database_config.password,
                port = database_config.port
            )
            
            connection_cursor = connection.cursor()

            return connection, connection_cursor
        except psycopg2.DatabaseError as exception:
            print('!>> {}'.format(exception))
            return None, None

def main():
    if len(sys.argv) < 2:
        print('!!> Please provide path to the configuration file as an argument to the script')
        return

    configuration_file_path = sys.argv[1]
    print('>>> Configuration file path was set to: {}'.format(configuration_file_path))

    print('>>> Initiating syncronizator')
    syncronizator = Syncronizator()

    print('>>> Loading syncronizator config')
    if not syncronizator.load_config(configuration_file_path):
        print('!!> Syncronizator config loading failed')
        return
    
    print('>>> Starting database synchronization')
    if syncronizator.synchronize():
        print('>>> Synchronization was successful')
        return

    print('!!> Synchronization failed')

if __name__ == '__main__':
    main()