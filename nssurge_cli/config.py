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
    help=f"Write an example config file to {str(DEFAULT_CONFIG_PATH)}")):
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
        DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_CONFIG_PATH.touch()
        with open(DEFAULT_CONFIG_PATH, 'w') as fp:
            config.write(fp)
            typer.secho(f"Wrote example config to {str(DEFAULT_CONFIG_PATH)}",
                        fg="green")
    else:
        config.write(sys.stdout)


@app.command('edit')
def edit_config(config_path: Path = DEFAULT_CONFIG_PATH):
    """
    Edit the config file.
    """
    typer.launch(str(config_path))


@app.command('show')
def show_config(config_path: Path = DEFAULT_CONFIG_PATH):
    """
    Show the config file.
    """
    config = read_config(config_path)
    typer.echo(f"SURGE_HTTP_API_ENDPOINT: {config['SURGE_HTTP_API_ENDPOINT']}")
    typer.echo(f"SURGE_HTTP_API_KEY: {config['SURGE_HTTP_API_KEY']}")
