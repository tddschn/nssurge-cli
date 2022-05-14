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

app = typer.Typer(name='modules')

async def get_modules():
    async with SurgeAPIClient(*get_creds()) as client:
        modules = await client.get_modules()
        return await modules.json()

@app.callback()
def get_modules_command():
    modules = asyncio.run(get_modules())
    typer_output_dict(modules)

async def set_modules()