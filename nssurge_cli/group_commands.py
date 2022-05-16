#!/usr/bin/env python3
from .config import get_config
from .utils import (
    typer_output_dict,
)

# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
from nssurge_api.types import (
    Policy,
    PolicyGroup,
)
import typer
import asyncio
from .policy_commands import complete_policy, complete_policy_for_policy_group

app = typer.Typer(name="group")


async def get_policy_group(policy_group: PolicyGroup = typer.Argument(None)) -> dict:
    """
    Get all policy groups, or a specific one.
    """
    async with SurgeAPIClient(*get_config()) as client:
        try:
            return await (await client.get_policy_group(policy_group)).json()
        except Exception as e:
            typer.secho(f"Error: {e}", err=True)
            typer.secho('Using proxy as an arg causes Surge for Mac to crash as of version 4.5.0', err=True, fg='red')
            return {}


# @app.command('group')
# @app.callback(invoke_without_command=True)
@app.command('policy')
def policy_group(# ctx: typer.Context,
    policy_group: PolicyGroup = typer.Argument(..., help="Policy group name", autocompletion=complete_policy),
    # output_json: bool = typer.Option(False, "--json", "-j"),
    # pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    # rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get all policy groups, or a specific one.
    """
    # if ctx.invoked_subcommand is not None:
    #     return
    policy_group_dict = asyncio.run(get_policy_group(policy_group))
    # typer_output_dict(policy_group_dict, output_json, pretty_print, rich_print)
    policy = policy_group_dict['policy']
    if policy is None:
        typer.echo(f"Policy group {policy_group} not found")
    else:
        typer.secho(f'The policy for group {policy_group} is {policy}')


async def get_policy_group_test_results() -> dict:
    """
    Get all policy groups, or a specific one.
    """
    async with SurgeAPIClient(*get_config()) as client:
        return await (await client.get_policy_group_test_results()).json()


@app.command("test-results")
def policy_group_test_results(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get all policy groups, or a specific one.
    """
    policy_group_test_dict = asyncio.run(get_policy_group_test_results())
    typer_output_dict(policy_group_test_dict, output_json, pretty_print, rich_print)


async def select_group(policy_group: PolicyGroup, policy: Policy):
    """
    Select a policy group.
    """
    async with SurgeAPIClient(*get_config()) as client:
        return await client.set_policy_group(policy_group, policy)


@app.command("select")
def select_group_command(policy: PolicyGroup = typer.Argument(..., help='Policy group name', autocompletion=complete_policy), policy_selected: Policy = typer.Argument(..., help='Policy name', autocompletion=complete_policy_for_policy_group)):
    """
    Select a policy group.
    """
    asyncio.run(select_group(policy, policy_selected))


async def test_policy_group(policy_group: PolicyGroup) -> dict:
    """
    Test a policy group.
    """
    async with SurgeAPIClient(*get_config()) as client:
        resp = await client.test_policy_group(policy_group)
        return await resp.json()


@app.command("test")
def test_policy_group_command(
    policy_group: PolicyGroup = typer.Argument(..., help="Policy group name", autocompletion=complete_policy),
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Test a policy group.
    """
    test_dict = asyncio.run(test_policy_group(policy_group))
    typer_output_dict(test_dict, output_json, pretty_print, rich_print)

@app.callback()
def group_command_callback():
    """For policy groups"""