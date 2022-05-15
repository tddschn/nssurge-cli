#!/usr/bin/env python3

from functools import cache
from pathlib import Path
import sys
from tkinter import getboolean
import typer

# mkdir -p ~/.nssurge-cli
# touch ~/.nssurge-cli/config.ini
DEFAULT_CONFIG_PATH = Path.home() / ".nssurge-cli" / "config.ini"
DEFAULT_SURGE_HTTP_API_ENDPOINT = "http://127.1:9999"
DEFAULT_TRUST_ENV = True

app = typer.Typer(name="config")


@cache
def read_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """
    Read the config file and return a dictionary of the contents.
    """
    import configparser

    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        "SURGE_HTTP_API_ENDPOINT": config.get("DEFAULT", "SURGE_HTTP_API_ENDPOINT", fallback=DEFAULT_SURGE_HTTP_API_ENDPOINT),
        "SURGE_HTTP_API_KEY": config["DEFAULT"]["SURGE_HTTP_API_KEY"],
        "TRUST_ENV": config.getboolean("DEFAULT", "TRUST_ENV", fallback=DEFAULT_TRUST_ENV),
    }


@app.command("example")
def write_example_config(
    write_config: bool = typer.Option(
        False,
        "--write",
        "-w",
        help=f"Write an example config file to {str(DEFAULT_CONFIG_PATH)}",
    )
):
    """
    Show example config.
    """
    import configparser

    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "SURGE_HTTP_API_ENDPOINT": DEFAULT_SURGE_HTTP_API_ENDPOINT,
        "SURGE_HTTP_API_KEY": "",
        "TRUST_ENV": DEFAULT_TRUST_ENV,
    }
    if write_config:
        DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_CONFIG_PATH.touch()
        with open(DEFAULT_CONFIG_PATH, "w") as fp:
            config.write(fp)
            typer.secho(
                f"Wrote example config to {str(DEFAULT_CONFIG_PATH)}", fg="green"
            )
    else:
        config.write(sys.stdout)


@app.command("edit")
def edit_config(config_path: Path = DEFAULT_CONFIG_PATH):
    """
    Edit the config file.
    """
    typer.launch(str(config_path))


@app.command("show")
def show_config(config_path: Path = DEFAULT_CONFIG_PATH):
    """
    Show the config file.
    """
    config = read_config(config_path)
    typer.echo(f"SURGE_HTTP_API_ENDPOINT: {config['SURGE_HTTP_API_ENDPOINT']}")
    typer.echo(f"SURGE_HTTP_API_KEY: {config['SURGE_HTTP_API_KEY']}")
    typer.echo(f"TRUST_ENV: {config['TRUST_ENV']}")


def get_config() -> tuple[str, str, bool]:
    config_dict = read_config()
    SURGE_HTTP_API_ENDPOINT = config_dict["SURGE_HTTP_API_ENDPOINT"]
    SURGE_HTTP_API_KEY = config_dict["SURGE_HTTP_API_KEY"]
    TRUST_ENV = config_dict["TRUST_ENV"]
    return SURGE_HTTP_API_ENDPOINT, SURGE_HTTP_API_KEY, TRUST_ENV
