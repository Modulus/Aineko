import yaml
import logging

logger = logging.getLogger("ConfigReader")


def read(config_file):
    logger.debug("Opening config file {}".format(config_file))
    with open(config_file, 'r') as stream:
        try:
            data = yaml.load(stream)
            logger.info("Found config data, returning")
            logger.debug("Data: {}".format(data))
            return data
        except yaml.YAMLError as error:
            logger.error(
                "Failed to read config data, fatal error: {}".format(error))
            print(error)
