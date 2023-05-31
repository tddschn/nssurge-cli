#!/usr/bin/env python3

from nssurge_cli.config import get_config
from nssurge_cli.utils import typer_output_dict

# use_local_nssurge_api_module()
from nssurge_api.api import SurgeAPIClient
from nssurge_api.types import LogLevel
import typer
import asyncio

# from nssurge_cli.cli import app


async def stop_engine():
    """
    Stop the engine and quit the app
    """
    async with SurgeAPIClient(*get_config()) as client:
        stop_resp = await client.stop_engine()
        stop_dict: dict = await stop_resp.json()
        # if 'error' in stop_dict:
        # if not stop_dict:
        # 	typer.secho(f'Failed to stop engine: {stop_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return stop_dict


# @app.command("stop")
def stop_engine_command():
    """
    Stop the engine
    """
    stop_dict = asyncio.run(stop_engine())
    typer_output_dict(stop_dict)


async def get_events():
    """
    Get events
    """
    async with SurgeAPIClient(*get_config()) as client:
        events_resp = await client.get_events()
        events_dict: dict = await events_resp.json()
        # if 'error' in events_dict:
        # if not events_dict:
        # 	typer.secho(f'Failed to get events: {events_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return events_dict


# @app.command("events")
def events(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get events
    """
    events_dict = asyncio.run(get_events())
    typer_output_dict(events_dict, output_json, pretty_print, rich_print)


async def get_rules():
    """
    Get rules
    """
    async with SurgeAPIClient(*get_config()) as client:
        rules_resp = await client.get_rules()
        rules_dict: dict = await rules_resp.json()
        # if 'error' in rules_dict:
        # if not rules_dict:
        # 	typer.secho(f'Failed to get rules: {rules_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return rules_dict


# @app.command("rules")
def rules(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get rules
    """
    rules_dict = asyncio.run(get_rules())
    typer_output_dict(rules_dict, output_json, pretty_print, rich_print)


async def get_traffic():
    """
    Get traffic
    """
    async with SurgeAPIClient(*get_config()) as client:
        traffic_resp = await client.get_traffic()
        traffic_dict: dict = await traffic_resp.json()
        # if 'error' in traffic_dict:
        # if not traffic_dict:
        # 	typer.secho(f'Failed to get traffic: {traffic_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return traffic_dict


# @app.command("traffic")
def traffic(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get traffic
    """
    traffic_dict = asyncio.run(get_traffic())
    typer_output_dict(traffic_dict, output_json, pretty_print, rich_print)


async def set_log_level(log_level: LogLevel):
    """
    Set log level
    """
    async with SurgeAPIClient(*get_config()) as client:
        log_level_resp = await client.set_log_level(log_level)
        log_level_dict: dict = await log_level_resp.json()
        # if 'error' in log_level_dict:
        # if not log_level_dict:
        # 	typer.secho(f'Failed to set log level: {log_level_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return log_level_dict


# doesn't seem to work
# def complete_loglevel(incomplete: str):
#     """
#     Complete log level
#     """
#     return [level.value for level in LogLevel if incomplete.lower() in level.value]


# @app.command("loglevel")
def set_log_level_command(log_level: LogLevel = typer.Argument(..., help="Log level")):
    """
    Set log level
    """
    log_level_dict = asyncio.run(set_log_level(log_level))
    typer_output_dict(log_level_dict)


def typer_register_misc_commands(app: typer.Typer):
    """
    Register misc commands
    """
    app.command('stop')(stop_engine_command)
    app.command('events')(events)
    app.command('rules')(rules)
    app.command('traffic')(traffic)
    app.command('loglevel')(set_log_level_command)
