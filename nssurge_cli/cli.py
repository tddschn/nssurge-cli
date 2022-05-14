from . import __version__, __app_name__
from .config import read_config, app as config_app
from .types import (OnOffToggleEnum)
from .utils import (bool2color, parse_cap_get, get_cap_state, use_local_nssurge_api_module)
from utils_tddschn.utils import strtobool
# use_local_nssurge_api_module()
from nssurge_api import SurgeAPIClient
from nssurge_api.types import (Capability, LogLevel, OutboundMode, Policy,
							   PolicyGroup, RequestsType, Profile, Enabled,
							   SetModuleStateRequest, EvalScriptMockRequest,
							   EvalCronScriptRequest, Script,
							   ChangeDeviceRequest) #, Policies)
import typer
import asyncio
from aiohttp import ClientSession, ClientResponse

app = typer.Typer(name=__app_name__)
app.add_typer(config_app)


def s2b(s: str) -> bool:
	return bool(strtobool(s))

def get_creds() -> tuple[str, str]:
	config_dict = read_config()
	SURGE_HTTP_API_ENDPOINT = config_dict["SURGE_HTTP_API_ENDPOINT"]
	SURGE_HTTP_API_KEY = config_dict["SURGE_HTTP_API_KEY"]
	return SURGE_HTTP_API_ENDPOINT, SURGE_HTTP_API_KEY


async def get_set_cap(
	capability: Capability, on_off: OnOffToggleEnum = typer.Argument(None)
) -> bool | tuple[bool, bool]:
	"""
	Get or set a capability.
	"""
	async with SurgeAPIClient(*get_creds()) as client:
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



@app.command('cap')
def cap(capability: Capability, on_off: OnOffToggleEnum = typer.Argument(None)):
	"""
	Get or set a capability.
	"""
	states = asyncio.run(get_set_cap(capability, on_off))
	if isinstance(states, bool):
		state_colored = typer.style(f"{states}", fg=bool2color(states))
		typer.secho(f"Capability {capability}: {state_colored}")
		# raise typer.Exit()
	else:
		states_colored = [typer.style(f'{state}', fg=bool2color(state)) for state in states]
		if on_off == OnOffToggleEnum.toggle:
			typer.secho(f"Toggled capability {capability}: {states_colored[0]} -> {states_colored[1]}")
		else:
			typer.secho(f"Set capability {capability}: {states_colored[0]} -> {states_colored[1]}")


async def get_caps() -> dict[str, bool]:
	"""get all caps"""
	async with SurgeAPIClient(*get_creds()) as client:
		# get caps concurrently
		caps = await asyncio.gather(*[
			get_cap_state(client, capability)
			for capability in Capability
		])
		return {capability.name: state for capability, state in zip(Capability, caps)}

@app.command('caps')
def caps():
	"""get all caps"""
	states = asyncio.run(get_caps())
	for capability, state in states.items():
		length = 16
		state_colored = typer.style(f"{state}", fg=bool2color(state))
		typer.secho(f"{capability:>{length}}: {state_colored}")


async def get_set_outbound(outbound_mode: OutboundMode = typer.Argument(None)) -> OutboundMode:
	"""
	Get or set the outbound mode.
	"""
	async with SurgeAPIClient(*get_creds()) as client:
		if outbound_mode is not None:
			set_resp = await client.set_outbound_mode(outbound_mode)
		new_outbound_mode = (await (await client.get_outbound_mode()).json())['mode']
		if outbound_mode is not None:
			typer.secho(f"Set outbound mode to {new_outbound_mode}")
		else:
			typer.secho(f"Current outbound mode: {new_outbound_mode}")
		return OutboundMode[new_outbound_mode]

@app.command('outbound')
def outbound(outbound_mode: OutboundMode = typer.Argument(None)):
	"""
	Get or set the outbound mode.
	"""
	asyncio.run(get_set_outbound(outbound_mode))

async def get_set_global_policy(policy: Policy = typer.Argument(None)) -> Policy:
	"""
	Get or set the global policy.
	"""
	async with SurgeAPIClient(*get_creds()) as client:
		if policy is not None:
			set_resp = await client.set_global_policy(policy)
			set_dict: dict = await set_resp.json()
			if 'error' in set_dict:
				typer.secho(f'Failed to set policy {policy}: {set_dict["error"]}', fg=typer.colors.RED)
				raise typer.Exit(1)
		current_policy = (await (await client.get_global_policy()).json())['policy']
		if policy is not None:
			typer.secho(f"Set global policy to {current_policy}")
		else:
			typer.secho(f"Current global policy: {current_policy}")
		return current_policy

@app.command('global')
def global_command(policy: Policy = typer.Argument(None)):
	"""
	Get or set the global policy.
	"""
	asyncio.run(get_set_global_policy(policy))
	typer.secho(f'Warning: the get API is broken on the Surge side')

async def get_policies():
	"""
	Get all policies.
	"""
	async with SurgeAPIClient(*get_creds()) as client:
		# get policies concurrently
		return await (await client.get_policy()).json()

@app.command('policies')
def policies(output_json: bool = typer.Option(False, '--json', '-j'), pretty_print: bool = typer.Option(False, '--pretty', '-p')):
	"""
	Get all policies.
	"""
	policies = asyncio.run(get_policies())
	if output_json:
		import json
		typer.secho(json.dumps(policies, indent=2))
	elif pretty_print:
		from pprint import PrettyPrinter
		pp = PrettyPrinter(indent=2)
		typer.secho(pp.pformat(policies))
	else:
		typer.secho(policies)


if __name__ == '__main__':
	app()
