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

                self.__main_database_config = config.DatabaseConfig(**database_configs[0])
                self.__follower_database_config = config.DatabaseConfig(**database_configs[1])

            return True
        except Exception as exception:
            print('!!> An exception ocurred:')
            print(exception)

            return False
    
    def synchronize(self):
        return True

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