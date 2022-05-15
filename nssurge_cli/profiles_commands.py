#!/usr/bin/env python3

from . import __version__, __app_name__, logger
from .config import read_config, app as config_app, get_creds
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

app = typer.Typer(name="profiles")


async def get_active_profile(mask_password: bool = True) -> dict:
    async with SurgeAPIClient(*get_creds()) as client:
        profile = await client.get_active_profile(mask_password)
        return await profile.json()


@app.callback(invoke_without_command=True)
def active_profile(ctx: typer.Context, mask_password: bool = True, output_json: bool = typer.Option(False, "--json", '-j'), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    """Get active profile"""
    if ctx.invoked_subcommand is not None:
        return
    profile = asyncio.run(get_active_profile(mask_password))
    typer_output_dict(profile, output_json, pretty_print, rich_print)


async def reload_profile():
    async with SurgeAPIClient(*get_creds()) as client:
        await client.reload_profile()


@app.command("reload")
def reload_profile_command():
    asyncio.run(reload_profile())


async def switch_profile(profile_name: Profile):
    async with SurgeAPIClient(*get_creds()) as client:
        await client.switch_profile(profile_name)


@app.command("switch")
def switch_profile_command(profile_name: Profile):
    asyncio.run(switch_profile(profile_name))


async def list_profiles():
    async with SurgeAPIClient(*get_creds()) as client:
        profiles = await client.get_profiles()
        return await profiles.json()


@app.command("list")
def list_profiles_command(output_json: bool = typer.Option(False, "--json", '-j'), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    profiles = asyncio.run(list_profiles())
    typer_output_dict(profiles, output_json, pretty_print, rich_print)


async def validate_profile(profile_name: Profile):
    async with SurgeAPIClient(*get_creds()) as client:
        resp = await client.validate_profile(profile_name)
        return await resp.json()


@app.command("validate")
def validate_profile_command(profile_name: Profile):
    profile = asyncio.run(validate_profile(profile_name))
    typer_output_dict(profile)
