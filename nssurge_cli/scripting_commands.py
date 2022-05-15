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

app = typer.Typer(name="script")


async def get_scripts():
    async with SurgeAPIClient(*get_config()) as client:
        scripting_resp = await client.get_scripts()
        return await scripting_resp.json()


@app.callback(invoke_without_command=True)
def scripts(ctx: typer.Context, output_json: bool = typer.Option(False, "--json", '-j'), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    """Get all scripts"""
    if ctx.invoked_subcommand is not None:
        return
    scripts_resp = asyncio.run(get_scripts())
    typer_output_dict(scripts_resp, output_json, pretty_print, rich_print)


async def eval_script_mock(**kwargs):
    req = EvalScriptMockRequest(**kwargs)
    async with SurgeAPIClient(*get_config()) as client:
        eval_script_mock_resp = await client.eval_script_mock(req)
        return await eval_script_mock_resp.json()


# todo: add eval-mock and eval-cron commands
# i don't use them so i'll leave them unimplemented for now
