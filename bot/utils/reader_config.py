import configparser
import os

def get_channel_id():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'channel.ini')
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config['Channel']['channel_id']


def update_channel_id(new_channel_id):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'channel.ini')
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    config['Channel']['channel_id'] = new_channel_id

    with open(config_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def get_urls(type_url: str):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'links.ini')
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config['Urls'][type_url]

def update_urls(type_url: str, new_url: str):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'links.ini')
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    config['Urls'][type_url] = new_url

    with open(config_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)