#!/usr/bin/env python3

from functools import cache
from pathlib import Path

# mkdir -p ~/.nssurge-cli
# touch ~/.nssurge-cli/config.ini
DEFAULT_CONFIG_PATH = Path.home() / ".nssurge-cli" / "config.ini"


@cache
def read_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """
	Read the config file and return a dictionary of the contents.
	"""
    import configparser
    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        "SURGE_HTTP_API_ENDPOINT":
        config["DEFAULT"]["SURGE_HTTP_API_ENDPOINT"],
        "SURGE_HTTP_API_KEY": config["DEFAULT"]["SURGE_HTTP_API_KEY"],
    }
