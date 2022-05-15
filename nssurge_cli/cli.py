from . import __version__, __app_name__, logger
from .config import read_config, app as config_app, get_creds
from .group_commands import app as group_app
from .cap_commands import app as cap_app
from .outbound_commands import app as outbound_app
from .global_commands import app as global_app
from .policy_commands import app as policy_app
from .test_commands import app as test_app
from .requests_commands import app as requests_app
from .profiles_commands import app as profiles_app
from .dns_commands import app as dns_app
from .modules_commands import app as modules_app
from .scripting_commands import app as scripting_app
from .devices_commands import app as devices_app
from .misc_commands import typer_register_misc_commands
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
app.add_typer(outbound_app)
app.add_typer(global_app)
app.add_typer(policy_app)
app.add_typer(test_app)
app.add_typer(requests_app)
app.add_typer(group_app)
app.add_typer(profiles_app)
app.add_typer(dns_app)
app.add_typer(modules_app)
app.add_typer(scripting_app)
app.add_typer(devices_app)
typer_register_misc_commands(app)






if __name__ == "__main__":
	app()
	print('main')
