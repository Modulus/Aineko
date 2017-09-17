import yaml
from core.config_reader import read

if __name__ == '__main__':
    data = read('config/sites')
    print(data)