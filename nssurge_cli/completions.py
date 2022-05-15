#!/usr/bin/env python3


from typing import Iterable
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
							   ChangeDeviceRequest, Policies, Proxy, Proxies, PolicyGroups)
import typer
import asyncio
from .policy_commands import get_policy
from aiohttp import ClientSession, ClientResponse



async def complete_policy(incomplete: str) -> Iterable[str]:
    """
    Complete policy names.
    """
    policy_dict: Policies = await get_policy()
    proxies: Proxies = policy_dict["proxies"]
    policy_groups: PolicyGroups = policy_dict["policy-groups"]
    
    return [p for p in proxies + policy_groups if incomplete in p]