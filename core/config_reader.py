import yaml


def read(config_file):
    with open(config_file, 'r') as stream:
        try:
            data = yaml.load(stream)
            return data
        except yaml.YAMLError as error:
            print(error)

