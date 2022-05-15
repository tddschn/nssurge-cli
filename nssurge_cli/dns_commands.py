#!/usr/bin/env python3

from . import __version__, __app_name__, logger
from .config import read_config, app as config_app, get_config
from .types import OnOffToggleEnum
from .utils import (
    bool2color,
    parse_cap_get,
    get_cap_state,
    typer_output_dict,
    use_local_nssurge_api_module,
)
from utils_tddschn.utils import strtobool

# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
from nssurge_api.types import (
    Capability,
    LogLevel,
    OutboundMode,
    Policy,
    PolicyGroup,
    RequestsType,
    Profile,
    Enabled,
    SetModuleStateRequest,
    EvalScriptMockRequest,
    EvalCronScriptRequest,
    Script,
    ChangeDeviceRequest,
    Policies,
    Proxy,
)
import typer
import asyncio
from aiohttp import ClientSession, ClientResponse

app = typer.Typer(name="dns")


async def flush_dns():
    async with SurgeAPIClient(*get_config()) as client:
        await client.flush_dns()


@app.command("flush")
def flush_dns_command():
    resp = asyncio.run(flush_dns())
    # resp is empty
    typer.secho(f'Flushed DNS cache', fg=typer.colors.GREEN)


async def get_dns():
    async with SurgeAPIClient(*get_config()) as client:
        dns = await client.get_dns()
        return await dns.json()


@app.callback(invoke_without_command=True)
def get_dns_command(ctx: typer.Context, output_json: bool = typer.Option(False, "--json", "-j"), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    if ctx.invoked_subcommand is not None:
        return
    dns = asyncio.run(get_dns())
    typer_output_dict(dns, output_json, pretty_print, rich_print)


async def test_dns():
    async with SurgeAPIClient(*get_config()) as client:
        resp = await client.test_dns()
        return await resp.json()


@app.command("test")
def test_dns_command(output_json: bool = typer.Option(False, "--json", "-j"), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    dns = asyncio.run(test_dns())
    typer_output_dict(dns, output_json, pretty_print, rich_print)
