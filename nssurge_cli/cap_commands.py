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

def s2b(s: str) -> bool:
    return bool(strtobool(s))


app = typer.Typer(name='cap')

async def get_set_cap(
    capability: Capability, on_off: OnOffToggleEnum = typer.Argument(None)
) -> bool | tuple[bool, bool]:
    """
    Get or set a capability.
    """
    async with SurgeAPIClient(*get_config()) as client:
        state_orig = await get_cap_state(client, capability)
        match on_off:
            case OnOffToggleEnum.on | OnOffToggleEnum.off:
                set_resp = await client.set_cap(capability, s2b(on_off))
            case OnOffToggleEnum.toggle:
                set_resp = await client.set_cap(capability, not state_orig)
            case _:
                return state_orig
        state_new = await get_cap_state(client, capability)
        return state_orig, state_new


# @app.command("cap")
@app.callback(invoke_without_command=True)
def cap(capability: Capability = typer.Argument(None), on_off: OnOffToggleEnum = typer.Argument(None)):
    """
    Get or set a capability.
    """
    if capability is None:
        caps()
        return
    states = asyncio.run(get_set_cap(capability, on_off))
    if isinstance(states, bool):
        state_colored = typer.style(f"{states}", fg=bool2color(states))
        typer.secho(f"Capability {capability}: {state_colored}")
        # raise typer.Exit()
    else:
        states_colored = [
            typer.style(f"{state}", fg=bool2color(state)) for state in states
        ]
        if on_off == OnOffToggleEnum.toggle:
            typer.secho(
                f"Toggled capability {capability}: {states_colored[0]} -> {states_colored[1]}"
            )
        else:
            typer.secho(
                f"Set capability {capability}: {states_colored[0]} -> {states_colored[1]}"
            )


async def get_caps() -> dict[str, bool]:
    """get all caps"""
    async with SurgeAPIClient(*get_config()) as client:
        # get caps concurrently
        caps = await asyncio.gather(
            *[get_cap_state(client, capability) for capability in Capability]
        )
        return {capability.name: state for capability, state in zip(Capability, caps)}


# @app.command("caps")
def caps():
    """get all caps"""
    states = asyncio.run(get_caps())
    for capability, state in states.items():
        length = 16
        state_colored = typer.style(f"{state}", fg=bool2color(state))
        typer.secho(f"{capability:>{length}}: {state_colored}")

