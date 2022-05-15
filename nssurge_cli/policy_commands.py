#!/usr/bin/env python3

from . import __version__, __app_name__, logger
from .config import read_config, app as config_app, get_config
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

app = typer.Typer(name="policy")

async def get_policy(policy: Policy = typer.Argument(None)) -> Policies | dict:
    """
    Get all policies.
    """
    async with SurgeAPIClient(*get_config()) as client:
        policy_dict = await (await client.get_policy(policy)).json()
        if policy is None:
            return policy_dict
        else:
            if "error" in policy:
                typer.secho(
                    f'Failed to get policy {policy}: {policy_dict["error"]}',
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
            return policy_dict


# @app.command("policy")
@app.callback(invoke_without_command=True)
def policy(ctx: typer.Context,
    policy: Policy = typer.Argument(None),
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get all policies, or a specific policy.
    """
    if ctx.invoked_subcommand is not None:
        return
    policy_dict = asyncio.run(get_policy(policy))
    typer_output_dict(policy_dict, output_json, pretty_print, rich_print)  # type: ignore

