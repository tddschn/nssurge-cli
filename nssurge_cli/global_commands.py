#!/usr/bin/env python3

from nssurge_cli.config import get_config

# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
from nssurge_api.types import Policy
import typer
import asyncio
from typing import Optional
from typing_extensions import Annotated

from nssurge_cli.policy_commands import complete_policy_and_proxy

app = typer.Typer(name="global")


async def get_set_global_policy(
    policy: Annotated[Optional[Policy], typer.Argument()] = None
) -> Policy:
    """
    Get or set the global policy.
    """
    async with SurgeAPIClient(*get_config()) as client:
        if policy is not None:
            set_resp = await client.set_global_policy(policy)
            set_dict: dict = await set_resp.json()
            if "error" in set_dict:
                typer.secho(
                    f'Failed to set policy {policy}: {set_dict["error"]}',
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
        current_policy = (await (await client.get_global_policy()).json())["policy"]
        if policy is not None:
            typer.secho(f"Set global policy to {current_policy}")
        else:
            typer.secho(f"Current global policy: {current_policy}")
        return current_policy


# @app.command("global")
@app.callback(invoke_without_command=True)
def global_command(
    ctx: typer.Context,
    policy: Policy = typer.Argument(
        None, help="Policy name", autocompletion=complete_policy_and_proxy
    ),
):
    """
    Get or set the global policy.
    """
    if ctx.invoked_subcommand is not None:
        return
    asyncio.run(get_set_global_policy(policy))
    # typer.secho(f"Warning: the get API is broken on the Surge side")
    # dimmed style
    typer.secho(
        f"Warning: the get API is broken on the Surge side, tested on Surge for Mac 4.5.0",
        dim=True,
        err=True,
    )
