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

app = typer.Typer(name="requests")

async def get_requests(requests_type: RequestsType = RequestsType.recent):
    """
    Get requests
    """
    async with SurgeAPIClient(*get_creds()) as client:
        req_resp = await client.get_requests(requests_type)
        req_dict: dict = await req_resp.json()
        # if 'error' in req_dict:
        # 	typer.secho(f'Failed to get requests: {req_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return req_dict


# @app.command("requests")
@app.callback(invoke_without_command=True)
def requests(ctx: typer.Context,
    requests_type: RequestsType = RequestsType.recent,
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get requests
    """
    if ctx.invoked_subcommand is not None:
        return
    req_dict = asyncio.run(get_requests(requests_type))
    typer_output_dict(req_dict, output_json, pretty_print, rich_print)


async def kill_request(request_id: int):
    """
    Kill requests
    """
    async with SurgeAPIClient(*get_creds()) as client:
        kill_resp = await client.kill_request(request_id)
        kill_dict: dict = await kill_resp.json()
        # if 'error' in kill_dict:
        # if not kill_dict:
        # 	typer.secho(f'Failed to kill requests: {kill_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return kill_dict


@app.command("kill")
def kill_request_command(request_id: int):
    """
    Kill requests
    """
    kill_dict = asyncio.run(kill_request(request_id))
    typer_output_dict(kill_dict)

