import configparser
import os
import sys
import logging

log = logging.getLogger()


def singleton(cls):
    _instance = {}

    def get_instance(*arg, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*arg, **kwargs)
        return _instance[cls]

    return get_instance


@singleton
class Config:
    def __init__(self) -> None:
        self._config = {}
        self.load_config()

    def load_config(self):
        config = configparser.ConfigParser()
        config_file = r"config.ini"
        if os.path.exists(config_file) is False:
            log.error("not find config.ini")
            sys.exit(1)
        config.read(config_file)

        self._config["host"] = config.get("Server", "host")
        self._config["port"] = config.get("Server", "port")
        self._config["platform"] = config.get("Server", "platform")
        self._config["currency"] = config.get("Currency", "currency").split(",")

    def get(self, key, default=None):
        return self._config.get(key, default)


if __name__ == "__main__":
    config = Config()
    config.load_config()
    print(f"Host: {config.get('host')}")
    print(f"Port: {config.get('port')}")
    print(f"Platform: {config.get('platform')}")
    print(f"Currency List: {config.get('currency')}")
