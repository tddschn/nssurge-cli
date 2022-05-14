#!/usr/bin/env python3


from . import __version__, __app_name__, logger
from .config import read_config, app as config_app, get_creds
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

app = typer.Typer(name='devices')

async def get_devices():
    async with SurgeAPIClient(*get_creds()) as client:
        devices_resp = await client.get_devices()
        return await devices_resp.json()

@app.callback()
def devices():
    devices_resp = asyncio.run(get_devices())
    typer_output_dict(devices_resp)

async def get_device_icon(icon_id):
    async with SurgeAPIClient(*get_creds()) as client:
        icon_resp = await client.get_device_icon(icon_id)
        return await icon_resp.json()

@app.command('icon')
def icon(icon_id):
    icon_resp = asyncio.run(get_device_icon(icon_id))
    typer_output_dict(icon_resp)

# todo: change_device unimplemented