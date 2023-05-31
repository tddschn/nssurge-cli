#!/usr/bin/env python3

from pathlib import Path
import typer
from aiohttp import ClientResponse
from nssurge_api import SurgeAPIClient
from nssurge_api.types import (
    Capability,
)

from utils_tddschn.utils import strtobool


def s2b(s: str) -> bool:
    return bool(strtobool(s))


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
    d: dict,
    output_json: bool = False,
    pretty_print: bool = False,
    rich_print: bool = False,
) -> None:
    if output_json:
        import json

        typer.secho(json.dumps(d, indent=2, ensure_ascii=False))
    elif pretty_print:
        from pprint import PrettyPrinter

        pp = PrettyPrinter(indent=2)
        typer.secho(pp.pformat(d))
    elif rich_print:
        try:
            from rich import print as rprint

            rprint(d)
        except ImportError:
            typer.secho("rich module not installed")
    else:
        typer.secho(d)


# typer_output_dict_typer_options = (    output_json: bool = typer.Option(False, "--json", "-j"),
#     pretty_print: bool = typer.Option(False, "--pretty", "-p"),)
rich_print: bool = (typer.Option(False, "--rich", "-r"),)  # type: ignore
