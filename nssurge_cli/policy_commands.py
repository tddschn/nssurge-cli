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
async def get_policy(policy: Policy | None = None) -> dict:
    """
    Get all policies.
    """
    async with SurgeAPIClient(*get_config()) as client:
        policy_dict = await (await client.get_policy(policy)).json()
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

def complete_policies(ctx: typer.Context, incomplete: str) -> Iterable[str]:
    """
    Complete policy names.
    """
    incomplete = incomplete.lower()
    policy_dict: Policies = asyncio.run(get_policy()) # type: ignore
    policies_already_supplied = ctx.params.get("policies") or []
    policy_groups: PolicyGroups = policy_dict["policy-groups"]
    return [p for p in policy_groups if incomplete in p.lower() and p not in policies_already_supplied]

def complete_proxies(ctx: typer.Context, incomplete: str) -> Iterable[str]:
    """
    Complete policy names.
    """
    incomplete = incomplete.lower()
    policy_dict: Policies = asyncio.run(get_policy()) # type: ignore
    policies_already_supplied = ctx.params.get("policies") or []
    policy_groups: PolicyGroups = policy_dict["proxies"]
    return [p for p in policy_groups if incomplete in p.lower() and p not in policies_already_supplied]

def complete_proxy(incomplete: str) -> Iterable[tuple[str, str]]:
    """
    Complete policy names.
    """
    incomplete = incomplete.lower()
    policy_dict: Policies = asyncio.run(get_policy()) # type: ignore
    proxies: Proxies = policy_dict["proxies"]
    # policy_groups: PolicyGroups = policy_dict["policy-groups"]
    # p2type_mapping = {p: 'policy group' for p in policy_groups if incomplete in p.lower()}
    p2type_mapping = {p: 'proxy' for p in proxies if incomplete in p.lower()}
    
    return p2type_mapping.items()

def complete_policy_and_proxy(incomplete: str) -> Iterable[tuple[str, str]]:
    """
    Complete policy names.
    """
    incomplete = incomplete.lower()
    policy_dict: Policies = asyncio.run(get_policy()) # type: ignore
    proxies: Proxies = policy_dict["proxies"]
    policy_groups: PolicyGroups = policy_dict["policy-groups"]
    p2type_mapping = {p: 'policy group' for p in policy_groups if incomplete in p.lower()}
    p2type_mapping.update({p: 'proxy' for p in proxies if incomplete in p.lower()})
    
    return p2type_mapping.items()

def complete_policy_for_policy_group(ctx: typer.Context, incomplete: str) -> Iterable[str]:
    """
    Complete policy names.
    """
    policy = ctx.params.get('policy')

    # like 'Netflix = select, Proxy, Direct'
    try:
        policy_rule_for_group: str = asyncio.run(get_policy(policy=policy))[policy]
    except:
        typer.secho(f'No policy found for policy group {policy}', fg='red', err=True)
        return []
    policies_str = policy_rule_for_group.split('=')[1].strip()
    import re
    policies: list[str] = re.split(r'\s*,\s*', policies_str)

    return [p for p in policies if incomplete.lower() in p.lower()]

# @app.command("policy")
@app.callback(invoke_without_command=True)
def policy(ctx: typer.Context,
    policy: Policy = typer.Argument(None, autocompletion=complete_policy),
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get all policies, or a specific policy
    """
    if ctx.invoked_subcommand is not None:
        return
    policy_dict = asyncio.run(get_policy(policy))
    if policy is None:
        # return policy_dict
        pass
    else:
        if "error" in policy_dict:
            typer.secho(
                f'Failed to get policy {policy}: {policy_dict["error"]}',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        # return policy_dict
    typer_output_dict(policy_dict, output_json, pretty_print, rich_print)  # type: ignore

