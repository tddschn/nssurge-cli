#!/usr/bin/env python3

from . import __version__, __app_name__, logger
from .config import read_config, app as config_app, get_creds
from .types import (OnOffToggleEnum)
from .utils import (bool2color, parse_cap_get, get_cap_state, typer_output_dict, use_local_nssurge_api_module)
from utils_tddschn.utils import strtobool
# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
from nssurge_api.types import (Capability, LogLevel, OutboundMode, Policy,
							   PolicyGroup, RequestsType, Profile, Enabled,
							   SetModuleStateRequest, EvalScriptMockRequest,
							   EvalCronScriptRequest, Script,
							   ChangeDeviceRequest, Policies, Proxy)
import typer
import asyncio
from aiohttp import ClientSession, ClientResponse

app = typer.Typer(name="test")

async def test_proxies(policies: list[Proxy], url: str | None = None) -> dict:
    """
    Test proxies
    """
    async with SurgeAPIClient(*get_creds()) as client:
        test_resp = await client.test_policies(policies, url)
        test_dict: dict = await test_resp.json()
        # if 'error' in test_dict:
        if not test_dict:
            typer.secho(
                f'Failed to test policies: {test_dict["error"]}', fg=typer.colors.RED
            )
            typer.secho("Please specify at least 1 valid proxy to test")
            raise typer.Exit(1)
        return test_dict


# @app.command("test")
@app.callback(invoke_without_command=True)
def test_proxies_command(ctx: typer.Context, policies: list[Proxy], url: str | None = None, output_json: bool = typer.Option(False, "--json", "-j"), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    """
    Test proxies
    """
    if ctx.invoked_subcommand is not None:
        return
    test_dict = asyncio.run(test_proxies(policies, url))
    typer_output_dict(test_dict, output_json, pretty_print, rich_print)  # type: ignore
