#!/usr/bin/env python3

from nssurge_cli.config import get_config
from nssurge_cli.types import ChangeDeviceEnum
from nssurge_cli.utils import (
    typer_output_dict,
)

# use_local_nssurge_api_module()
from nssurge_api.api import SurgeAPIClient
from nssurge_api.types import (
    ChangeDeviceRequest,
)
import typer
import asyncio

app = typer.Typer(name="devices")


async def get_devices():
    async with SurgeAPIClient(*get_config()) as client:
        devices_resp = await client.get_devices()
        return await devices_resp.json()


def complete_devices(incomplete: str):
    """
    Complete device names.
    """
    incomplete = incomplete.lower()
    devices_dict = asyncio.run(get_devices())  # type: ignore
    devices: list[dict] = devices_dict['devices']
    for device in devices:
        info = ' | '.join(
            map(
                lambda x: str(device.get(x)), ['name', 'displayIPAddress', 'totalBytes']
            )
        )
        id: str = device.get('identifier')  # type: ignore
        if incomplete in id or incomplete in info.lower():
            yield id, info


@app.callback(invoke_without_command=True)
def devices(
    ctx: typer.Context,
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """Manage devices"""
    if ctx.invoked_subcommand is not None:
        return
    devices_resp = asyncio.run(get_devices())
    typer_output_dict(devices_resp, output_json, pretty_print, rich_print)


async def get_device_icon(icon_id):
    async with SurgeAPIClient(*get_config()) as client:
        icon_resp = await client.get_device_icon(icon_id)
        return await icon_resp.json()


@app.command("icon")
def icon(
    icon_id,
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    icon_resp = asyncio.run(get_device_icon(icon_id))
    typer_output_dict(icon_resp, output_json, pretty_print, rich_print)
    typer.secho(
        'Warning: the Surge API used is broken on Surge for mac 4.5.0',
        dim=True,
        err=True,
    )


async def change_device(req: ChangeDeviceRequest):
    async with SurgeAPIClient(*get_config()) as client:
        resp = await client.change_device(req)
        return await resp.json()


@app.command('set')
def set_device_command(
    physical_address: str = typer.Argument(..., autocompletion=complete_devices),
    field: ChangeDeviceEnum = typer.Argument(...),
    value: str = typer.Argument(...),
):
    req = ChangeDeviceRequest(
        physicalAddress=physical_address,
    )
    # setattr(req, field.value, value)
    req[field.value] = value
    resp_dict = asyncio.run(change_device(req))
    # typer_output_dict(resp_dict)
    if not resp_dict:
        # success
        typer.secho(
            f'Successfully set {field.value} to {value} for {physical_address}',
            fg=typer.colors.GREEN,
        )
    else:
        # failure
        typer.secho(
            f'Failed to set {field.value} to {value} for {physical_address}',
            fg=typer.colors.RED,
        )
        typer.secho(f'Error: {resp_dict["error"]}', fg=typer.colors.RED)
