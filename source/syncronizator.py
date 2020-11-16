import sys
import psycopg2

class Syncronizator():
    def __init__(self):
        super().__init__()
    
    def load_config(self, config_file_path):
        try:
            return True
        except Exception as exception:
            print('!!> An exception ocurred:')
            print(exception)

            return False
    
    def syncronize(self):
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
    
    print('>>> ')

if __name__ == '__main__':
    main()