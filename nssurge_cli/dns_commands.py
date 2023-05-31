#!/usr/bin/env python3

from nssurge_cli.config import get_config
from nssurge_cli.utils import (
    typer_output_dict,
)

# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
import typer
import asyncio

app = typer.Typer(name="dns")


async def flush_dns():
    async with SurgeAPIClient(*get_config()) as client:
        await client.flush_dns()


@app.command("flush")
def flush_dns_command():
    resp = asyncio.run(flush_dns())
    # resp is empty
    typer.secho(f'Flushed DNS cache', fg=typer.colors.GREEN)


async def get_dns():
    async with SurgeAPIClient(*get_config()) as client:
        dns = await client.get_dns()
        return await dns.json()


@app.callback(invoke_without_command=True)
def get_dns_command(ctx: typer.Context, output_json: bool = typer.Option(False, "--json", "-j"), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    """Manage DNS"""
    if ctx.invoked_subcommand is not None:
        return
    dns = asyncio.run(get_dns())
    typer_output_dict(dns, output_json, pretty_print, rich_print)


async def test_dns():
    async with SurgeAPIClient(*get_config()) as client:
        resp = await client.test_dns()
        return await resp.json()


@app.command("test")
def test_dns_command(output_json: bool = typer.Option(False, "--json", "-j"), pretty_print: bool = typer.Option(False, "--pretty", "-p"), rich_print: bool = typer.Option(False, "--rich", "-r")):
    dns = asyncio.run(test_dns())
    typer_output_dict(dns, output_json, pretty_print, rich_print)
