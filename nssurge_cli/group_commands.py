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

app = typer.Typer(name="group")


async def get_policy_group(policy_group: PolicyGroup = typer.Argument(None)) -> dict:
    """
    Get all policy groups, or a specific one.
    """
    async with SurgeAPIClient(*get_creds()) as client:
        return await (await client.get_policy_group(policy_group)).json()


# @app.command('group')
@app.callback()
def policy_group(
    policy_group: PolicyGroup,
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
):
    """
    Get all policy groups, or a specific one.
    """
    policy_group_dict = asyncio.run(get_policy_group(policy_group))
    typer_output_dict(policy_group_dict, output_json, pretty_print)


async def get_policy_group_test_results() -> dict:
    """
    Get all policy groups, or a specific one.
    """
    async with SurgeAPIClient(*get_creds()) as client:
        return await (await client.get_policy_group_test_results()).json()


@app.command("test-results")
def policy_group_test_results(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
):
    """
    Get all policy groups, or a specific one.
    """
    policy_group_test_dict = asyncio.run(get_policy_group_test_results())
    typer_output_dict(policy_group_test_dict, output_json, pretty_print)


async def select_group(policy_group: PolicyGroup, policy: Policy):
    """
    Select a policy group.
    """
    async with SurgeAPIClient(*get_creds()) as client:
        return await client.set_policy_group(policy_group, policy)


@app.command("select")
def select_group_command(policy_group: PolicyGroup, policy: Policy):
    """
    Select a policy group.
    """
    asyncio.run(select_group(policy_group, policy))


async def test_policy_group(policy_group: PolicyGroup) -> dict:
    """
    Test a policy group.
    """
    async with SurgeAPIClient(*get_creds()) as client:
        resp = await client.test_policy_group(policy_group)
        return await resp.json()


@app.command("test")
def test_policy_group_command(
    policy_group: PolicyGroup,
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
):
    """
    Test a policy group.
    """
    test_dict = asyncio.run(test_policy_group(policy_group))
    typer_output_dict(test_dict, output_json, pretty_print)
