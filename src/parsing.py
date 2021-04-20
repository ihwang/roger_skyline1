import configparser


def parser(CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config['ROGER_SKYLINE_1']