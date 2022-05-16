#!/usr/bin/env python3

from pathlib import Path
from typing import Iterable
from .config import get_config
from .utils import typer_output_dict
# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
from nssurge_api.types import RequestsType
import typer
import asyncio

app = typer.Typer(name="requests")

async def get_requests(requests_type: RequestsType = RequestsType.recent):
    """
    Get requests
    """
    async with SurgeAPIClient(*get_config()) as client:
        req_resp = await client.get_requests(requests_type)
        req_dict: dict = await req_resp.json()
        # if 'error' in req_dict:
        # 	typer.secho(f'Failed to get requests: {req_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return req_dict

def complete_requests_id(incomplete: str) -> Iterable[tuple[str, str]]:
    """
    Complete requests ids.
    """
    incomplete = incomplete.lower()
    req_dict: dict = asyncio.run(get_requests(requests_type=RequestsType.active)) # type: ignore
    reqs: list[dict] = req_dict["requests"]
    for req in reqs:
        info = Path(req['processPath']).name
        info += ' | '
        info += ' | '.join(map(lambda x: req.get(x, ''), ['status', 'policyName', 'rule', 'URL']))
        if incomplete in str(req['id']) or incomplete in info.lower():
            yield (str(req['id']), info)
    

# @app.command("requests")
@app.callback(invoke_without_command=True)
def requests(ctx: typer.Context,
    requests_type: RequestsType = typer.Option(RequestsType.recent, '--type', '-t'),
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get requests
    """
    if ctx.invoked_subcommand is not None:
        return
    req_dict = asyncio.run(get_requests(requests_type))
    typer_output_dict(req_dict, output_json, pretty_print, rich_print)


async def kill_request(request_id: int):
    """
    Kill requests
    """
    async with SurgeAPIClient(*get_config()) as client:
        kill_resp = await client.kill_request(request_id)
        kill_dict: dict = await kill_resp.json()
        # if 'error' in kill_dict:
        # if not kill_dict:
        # 	typer.secho(f'Failed to kill requests: {kill_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return kill_dict


@app.command("kill")
def kill_request_command(request_id: int = typer.Argument(..., help="Request ID", autocompletion=complete_requests_id)):
    """
    Kill requests
    """
    kill_dict = asyncio.run(kill_request(request_id))
    error = kill_dict.get('error', None)
    if error is None:
        # success
        typer.secho(f'Successfully killed request {request_id}', fg=typer.colors.GREEN)
    else:
        # failed
        typer.secho(f'Failed to kill request {request_id}', fg=typer.colors.RED)
        typer.secho(f'Error: {error}', fg=typer.colors.RED)

