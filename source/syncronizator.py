import sys
import json
import psycopg2
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
                
            return True
        except Exception as exception:
            print('!!> An exception ocurred:')
            print('!!> \"{}\"'.format(exception))

            return False
    
    def synchronize(self):
        print('>>> Scanning main database')
        self.scan_database(self.__main_database_configuration)
        
        return True

    def scan_database(self, database_config):
        scan_command = 'PGPASSWORD={} pg_dump -h {} -U {} {} > scan.sql'.format(database_config.password, database_config.host, database_config.user, database_config.name)        
        subprocess.call(scan_command, shell=True)

        print(">>> Built finished")

    def build_database(self, database_config):
        build_command = 'psql pg_restore -h {} -U {} -d {} < scan.sql'.format(database_config.host, database_config.user, database_config.name)
        subprocess.call(build_command, shell=True)

        print(">>> Built finished")

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