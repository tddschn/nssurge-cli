#!/usr/bin/env python3

from functools import cache
from typing import Iterable
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
							   ChangeDeviceRequest, Policies, Proxy, Proxies, PolicyGroups)
import typer
import asyncio
from aiohttp import ClientSession, ClientResponse
# from .completions import complete_policy

app = typer.Typer(name="policy")

@cache
async def get_policy(policy: Policy | None = None) -> Policies | dict:
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

def complete_policy(incomplete: str) -> Iterable[tuple[str, str]]:
    """
    Complete policy names.
    """
    incomplete = incomplete.lower()
    policy_dict: Policies = asyncio.run(get_policy()) # type: ignore
    # proxies: Proxies = policy_dict["proxies"]
    policy_groups: PolicyGroups = policy_dict["policy-groups"]
    p2type_mapping = {p: 'policy group' for p in policy_groups if incomplete in p.lower()}
    # p2type_mapping = {p: 'proxy' for p in proxies if incomplete in p.lower()}
    
    return p2type_mapping.items()


# @app.command("policy")
@app.callback(invoke_without_command=True)
def policy(ctx: typer.Context,
    policy: Policy = typer.Argument(None, autocompletion=complete_policy),
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

