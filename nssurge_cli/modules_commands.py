#!/usr/bin/env python3

from nssurge_cli.cap_commands import s2b
from nssurge_cli.config import get_config
from nssurge_cli.types import OnOffToggleEnum
from nssurge_cli.utils import typer_output_dict, s2b

# use_local_nssurge_api_module()
from nssurge_api.api import SurgeAPIClient
from nssurge_api.types import SetModuleStateRequest, Module
import typer
import asyncio

app = typer.Typer(name="modules")


async def get_modules():
    async with SurgeAPIClient(*get_config()) as client:
        modules = await client.get_modules()
        return await modules.json()


def complete_module(incomplete: str):
    incomplete = incomplete.lower()
    modules = asyncio.run(get_modules())
    modules_available: list[str] = modules['available']
    modules_enabled: list[str] = modules['enabled']
    for module in modules_available:
        if incomplete in module:
            if module in modules_enabled:
                yield module, 'enabled'
            else:
                yield module, 'disabled'


@app.callback(invoke_without_command=True)
def get_modules_command(
    ctx: typer.Context,
    output_json: bool = typer.Option(False, "--json", '-j'),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """Manage modules"""
    if ctx.invoked_subcommand is not None:
        return
    modules = asyncio.run(get_modules())
    typer_output_dict(modules, output_json, pretty_print, rich_print)


async def set_modules(config: SetModuleStateRequest):
    async with SurgeAPIClient(*get_config()) as client:
        resp = await client.set_modules(config)
        return await resp.json()


@app.command('set')
def set_modules_command(
    module: Module = typer.Argument(
        ..., help="Module to set", autocompletion=complete_module
    ),
    state: OnOffToggleEnum = typer.Argument(..., help="State to set"),
):
    """Set module state"""
    config: SetModuleStateRequest = {module: s2b(state)}
    set_dict = asyncio.run(set_modules(config))
    if 'error' not in set_dict:
        typer.secho(f"Set module {module} to {state}", fg='green')
    else:
        typer.secho(f"Error: {set_dict['error']}", fg='red')
