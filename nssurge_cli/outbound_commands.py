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

app = typer.Typer(name="outbound")

async def get_set_outbound(
    outbound_mode: OutboundMode = typer.Argument(None),
) -> OutboundMode:
    """
    Get or set the outbound mode.
    """
    async with SurgeAPIClient(*get_config()) as client:
        if outbound_mode is not None:
            set_resp = await client.set_outbound_mode(outbound_mode)
        new_outbound_mode = (await (await client.get_outbound_mode()).json())["mode"]
        match new_outbound_mode:
            case 'direct':
                color = 'green'
            case 'proxy':
                color = 'yellow'
            case 'rule':
                color = 'blue'
            case _:
                raise ValueError(f"Unknown outbound mode: {new_outbound_mode}")
        new_outbound_mode_colored = typer.style(new_outbound_mode, fg=color)
        if outbound_mode is not None:
            typer.secho(f"Set outbound mode to {new_outbound_mode_colored}")
        else:
            typer.secho(f"Current outbound mode: {new_outbound_mode_colored}")
        return OutboundMode[new_outbound_mode]


# @app.command("outbound")
@app.callback(invoke_without_command=True)
def outbound(ctx: typer.Context, outbound_mode: OutboundMode = typer.Argument(None)):
    """
    Get or set the outbound mode.
    """
    if ctx.invoked_subcommand is not None:
        return
    asyncio.run(get_set_outbound(outbound_mode))
