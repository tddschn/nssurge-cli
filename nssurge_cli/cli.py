from . import __version__, __app_name__, logger
from .config import read_config, app as config_app, get_creds
from .group_commands import app as group_app
from .cap_commands import app as cap_app
from .profiles_commands import app as profiles_app
from .dns_commands import app as dns_app
from .modules_commands import app as modules_app
from .scripting_commands import app as scripting_app
from .devices_commands import app as devices_app
from .types import OnOffToggleEnum
from .utils import (
    bool2color,
    parse_cap_get,
    get_cap_state,
    typer_output_dict,
    use_local_nssurge_api_module,
)
from utils_tddschn.utils import strtobool

# use_local_nssurge_api_module()
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
    Policies,
    Proxy,
)
import typer
import asyncio
from aiohttp import ClientSession, ClientResponse

app = typer.Typer(name=__app_name__)
app.add_typer(config_app)
app.add_typer(cap_app)
app.add_typer(group_app)
app.add_typer(profiles_app)
app.add_typer(dns_app)
app.add_typer(modules_app)
app.add_typer(scripting_app)
app.add_typer(devices_app)


async def get_set_outbound(
    outbound_mode: OutboundMode = typer.Argument(None),
) -> OutboundMode:
    """
    Get or set the outbound mode.
    """
    async with SurgeAPIClient(*get_creds()) as client:
        if outbound_mode is not None:
            set_resp = await client.set_outbound_mode(outbound_mode)
        new_outbound_mode = (await (await client.get_outbound_mode()).json())["mode"]
        if outbound_mode is not None:
            typer.secho(f"Set outbound mode to {new_outbound_mode}")
        else:
            typer.secho(f"Current outbound mode: {new_outbound_mode}")
        return OutboundMode[new_outbound_mode]


@app.command("outbound")
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
            if "error" in set_dict:
                typer.secho(
                    f'Failed to set policy {policy}: {set_dict["error"]}',
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
        current_policy = (await (await client.get_global_policy()).json())["policy"]
        if policy is not None:
            typer.secho(f"Set global policy to {current_policy}")
        else:
            typer.secho(f"Current global policy: {current_policy}")
        return current_policy


@app.command("global")
def global_command(policy: Policy = typer.Argument(None)):
    """
    Get or set the global policy.
    """
    asyncio.run(get_set_global_policy(policy))
    typer.secho(f"Warning: the get API is broken on the Surge side")


async def get_policy(policy: Policy = typer.Argument(None)) -> Policies | dict:
    """
    Get all policies.
    """
    async with SurgeAPIClient(*get_creds()) as client:
        policy_dict = await (await client.get_policy(policy)).json()
        if policy is None:
            return policy_dict
        else:
            if "error" in policy:
                typer.secho(
                    f'Failed to get policy {policy}: {policy_dict["error"]}',
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
            return policy_dict


@app.command("policy")
def policy(
    policy: Policy = typer.Argument(None),
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get all policies, or a specific policy.
    """
    policy_dict = asyncio.run(get_policy(policy))
    typer_output_dict(policy_dict, output_json, pretty_print, rich_print)  # type: ignore


async def test_proxies(policies: list[Proxy], url: str | None = None) -> dict:
    """
    Test proxies
    """
    async with SurgeAPIClient(*get_creds()) as client:
        test_resp = await client.test_policies(policies, url)
        test_dict: dict = await test_resp.json()
        # if 'error' in test_dict:
        if not test_dict:
            typer.secho(
                f'Failed to test policies: {test_dict["error"]}', fg=typer.colors.RED
            )
            typer.secho("Please specify at least 1 valid proxy to test")
            raise typer.Exit(1)
        return test_dict


@app.command("test")
def test_proxies_command(policies: list[Proxy], url: str | None = None):
    """
    Test proxies
    """
    test_dict = asyncio.run(test_proxies(policies, url))
    typer_output_dict(test_dict)


async def get_requests(requests_type: RequestsType = RequestsType.recent):
    """
    Get requests
    """
    async with SurgeAPIClient(*get_creds()) as client:
        req_resp = await client.get_requests(requests_type)
        req_dict: dict = await req_resp.json()
        # if 'error' in req_dict:
        # 	typer.secho(f'Failed to get requests: {req_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return req_dict


@app.command("requests")
def requests(
    requests_type: RequestsType = RequestsType.recent,
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get requests
    """
    req_dict = asyncio.run(get_requests(requests_type))
    typer_output_dict(req_dict, output_json, pretty_print, rich_print)


async def kill_request(request_id: int):
    """
    Kill requests
    """
    async with SurgeAPIClient(*get_creds()) as client:
        kill_resp = await client.kill_request(request_id)
        kill_dict: dict = await kill_resp.json()
        # if 'error' in kill_dict:
        # if not kill_dict:
        # 	typer.secho(f'Failed to kill requests: {kill_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return kill_dict


@app.command("kill")
def kill_request_command(request_id: int):
    """
    Kill requests
    """
    kill_dict = asyncio.run(kill_request(request_id))
    typer_output_dict(kill_dict)


async def stop_engine():
    """
    Stop the engine
    """
    async with SurgeAPIClient(*get_creds()) as client:
        stop_resp = await client.stop_engine()
        stop_dict: dict = await stop_resp.json()
        # if 'error' in stop_dict:
        # if not stop_dict:
        # 	typer.secho(f'Failed to stop engine: {stop_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return stop_dict


@app.command("stop")
def stop_engine_command():
    """
    Stop the engine
    """
    stop_dict = asyncio.run(stop_engine())
    typer_output_dict(stop_dict)


async def get_events():
    """
    Get events
    """
    async with SurgeAPIClient(*get_creds()) as client:
        events_resp = await client.get_events()
        events_dict: dict = await events_resp.json()
        # if 'error' in events_dict:
        # if not events_dict:
        # 	typer.secho(f'Failed to get events: {events_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return events_dict


@app.command("events")
def events(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get events
    """
    events_dict = asyncio.run(get_events())
    typer_output_dict(events_dict, output_json, pretty_print, rich_print)


async def get_rules():
    """
    Get rules
    """
    async with SurgeAPIClient(*get_creds()) as client:
        rules_resp = await client.get_rules()
        rules_dict: dict = await rules_resp.json()
        # if 'error' in rules_dict:
        # if not rules_dict:
        # 	typer.secho(f'Failed to get rules: {rules_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return rules_dict


@app.command("rules")
def rules(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get rules
    """
    rules_dict = asyncio.run(get_rules())
    typer_output_dict(rules_dict, output_json, pretty_print, rich_print)


async def get_traffic():
    """
    Get traffic
    """
    async with SurgeAPIClient(*get_creds()) as client:
        traffic_resp = await client.get_traffic()
        traffic_dict: dict = await traffic_resp.json()
        # if 'error' in traffic_dict:
        # if not traffic_dict:
        # 	typer.secho(f'Failed to get traffic: {traffic_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return traffic_dict


@app.command("traffic")
def traffic(
    output_json: bool = typer.Option(False, "--json", "-j"),
    pretty_print: bool = typer.Option(False, "--pretty", "-p"),
    rich_print: bool = typer.Option(False, "--rich", "-r"),
):
    """
    Get traffic
    """
    traffic_dict = asyncio.run(get_traffic())
    typer_output_dict(traffic_dict, output_json, pretty_print, rich_print)


async def set_log_level(log_level: LogLevel):
    """
    Set log level
    """
    async with SurgeAPIClient(*get_creds()) as client:
        log_level_resp = await client.set_log_level(log_level)
        log_level_dict: dict = await log_level_resp.json()
        # if 'error' in log_level_dict:
        # if not log_level_dict:
        # 	typer.secho(f'Failed to set log level: {log_level_dict["error"]}', fg=typer.colors.RED)
        # 	raise typer.Exit(1)
        return log_level_dict


@app.command("loglevel")
def set_log_level_command(log_level: LogLevel):
    """
    Set log level
    """
    log_level_dict = asyncio.run(set_log_level(log_level))
    typer_output_dict(log_level_dict)


if __name__ == "__main__":
    app()
