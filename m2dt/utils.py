import configparser


def get_api_key(section, key="api_key", config_file="config.ini"):
    """Get the Youtube API key from a configuration file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.get(section, key)
