import os
import sys
import json
import config 
import subprocess

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
                
                print('>>> Loaded configurations: ')
                repr(self.__main_database_configuration)
                print(25 * '-' )
                repr(self.__follower_database_configuration)

            return True
        except Exception as exception:
            print('!!> An exception ocurred:')
            print('!!> \"{}\"'.format(exception))

            return False
    
    def synchronize(self):
        print('>>> Scanning main database')
        self.scan_database(self.__main_database_configuration)
        
        print('>>> Truncating tables in DB.')
        self.__truncate_tables(self.__follower_database_configuration)

        print('>>> Building follower database')
        self.build_database(self.__follower_database_configuration)
        return True

    def scan_database(self, database_config):
        scan_command = 'PGPASSWORD={} pg_dump -F t --inserts -h {} -U {} {} > scan.tar'.format(database_config.password, database_config.host, database_config.user, database_config.name)        
        subprocess.call(scan_command, shell=True)

        print(">>> Built finished")

    def build_database(self, database_config):
        build_command = 'PGPASSWORD={} pg_restore --create -h {} -U {} -d {} scan.tar'.format(database_config.password, database_config.host, database_config.user, database_config.name)
        subprocess.call(build_command, shell=True)

        os.remove('scan.tar')

        print(">>> Built finished")

    def __truncate_tables(self, database_config):
        get_tables_command = 'PGPASSWORD={} psql -h {} -U {} -d {} -c "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != \'pg_catalog\' AND schemaname != \'information_schema\';" -e nomedb >> tables.txt'.format(
            database_config.password,
            database_config.host, 
            database_config.user, 
            database_config.name
        )

        subprocess.call(get_tables_command, shell=True)
        print('>>> Table names were dumped.')

        tables_file_content = None

        with open('tables.txt', 'r') as tables_file:
            tables_file_content = tables_file.readlines()[4:]
        
        os.remove('tables.txt')

        for table in tables_file_content:
            if table.startswith('('):
                break
            table_name = table.replace(' ', '').replace('\n', '')

            truncate_tables_command = 'PGPASSWORD={} psql -h {} -U {} -d {} -c"TRUNCATE TABLE {};"'.format(
                database_config.password, 
                database_config.host, 
                database_config.user, 
                database_config.name, 
                table_name, 
            )
            subprocess.call(truncate_tables_command, shell=True)
        print('>>> Tables were truncated.')

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