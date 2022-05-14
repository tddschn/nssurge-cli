#!/usr/bin/env python3

from pathlib import Path
import typer
from aiohttp import ClientSession, ClientResponse
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
)


async def parse_cap_get(resp: ClientResponse) -> bool:
    if not resp.status == 200:
        raise ValueError(f"Unexpected status code: {resp.status}")
    return (await resp.json())["enabled"]


async def get_cap_state(client: SurgeAPIClient, capability: Capability) -> bool:
    get_resp = await client.get_cap(capability)
    orig_state = await parse_cap_get(get_resp)
    return orig_state


def bool2color(state: bool) -> str:
    if state:
        color = typer.colors.GREEN
    else:
        color = typer.colors.RED
    return color


def use_local_nssurge_api_module():
    import sys

    sys.path.insert(0, str(Path.home() / "testdir" / "nssurge-api"))
    print(sys.path)


def typer_output_dict(
    d: dict, output_json: bool = False, pretty_print: bool = False
) -> None:
    if output_json:
        import json

        typer.secho(json.dumps(d, indent=2))
    elif pretty_print:
        from pprint import PrettyPrinter

        pp = PrettyPrinter(indent=2)
        typer.secho(pp.pformat(d))
    else:
        typer.secho(d)
