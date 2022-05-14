#!/usr/bin/env python3

from functools import cache
from pathlib import Path
import sys
import typer

# mkdir -p ~/.nssurge-cli
# touch ~/.nssurge-cli/config.ini
DEFAULT_CONFIG_PATH = Path.home() / ".nssurge-cli" / "config.ini"
DEFAULT_SURGE_HTTP_API_ENDPOINT = 'http://127.1:9999'

app = typer.Typer(name='config')


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


@app.command('example')
def write_example_config(write_config: bool = typer.Option(
    False,
    "--write",
    "-w",
    help="Write an example config file to ~/.nssurge-cli/config.ini")):
    """
    Show example config.
    """
    import configparser
    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "SURGE_HTTP_API_ENDPOINT": DEFAULT_SURGE_HTTP_API_ENDPOINT,
        "SURGE_HTTP_API_KEY": "",
    }
    if write_config:
        with open(DEFAULT_CONFIG_PATH, 'w') as fp:
            config.write(fp)
    else:
        config.write(sys.stdout)