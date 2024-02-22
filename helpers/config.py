import os
import json
import logging
import logging.config
from dotenv import load_dotenv

#DOTENV Initialization
load_dotenv()

#Logger
LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_Loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "client": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

logger.info("Loading DISCORD TOKEN...")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN_ENV")


#Read and Write Functions
def read_channels_json() -> list[int]:
    with open("json/channels.json", "r") as channels_json:
        channels = json.load(channels_json)
    return channels

def write_channels_json(channels: list[int]) -> None:
    with open("json/channels.json", "w") as channels_json:
        channels = json.dump(channels, channels_json)

def read_usernames_json() -> list[str]:
    with open("json/usernames.json", "r") as usernames_json:
        usernames = json.load(usernames_json)
    return usernames

def write_usernames_json(usernames: list[str]) -> None:
    with open("json/usernames.json", "w") as usernames_json:
        usernames = json.dump(usernames, usernames_json)