#!/usr/bin/env python3

from nssurge_cli.config import get_config
from nssurge_cli.utils import typer_output_dict
# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
from nssurge_api.types import Proxy
import typer
import asyncio
from nssurge_cli.policy_commands import complete_proxies

app = typer.Typer(name="test")

async def test_proxies(policies: list[Proxy], url: str | None = None) -> dict:
    """
    Test proxies
    """
    async with SurgeAPIClient(*get_config()) as client:
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
def test_proxies_command(ctx: typer.Context, policies: list[Proxy] = typer.Argument(..., autocompletion=complete_proxies), url: str | None = None, output_json: bool = typer.Option(False, "--json", "-j"), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    """
    Test proxies
    """
    #! bug:
    # options after list of arguments interpreted as argument
    # https://github.com/tiangolo/typer/search?q=options%20after%20list%20of%20arguments%20interpreted%20as%20argument
    # changing the arg to option doesn't help either
    if ctx.invoked_subcommand is not None:
        return
    test_dict = asyncio.run(test_proxies(policies, url))
    typer_output_dict(test_dict, output_json, pretty_print, rich_print)  # type: ignore
