from . import __version__, __app_name__
from .config import read_config, app as config_app
from .types import (OnOffEnum)
from utils_tddschn.utils import strtobool # type: ignore
from nssurge_api import SurgeAPIClient
from nssurge_api.types import (Capability, LogLevel, OutboundMode, Policy, PolicyGroup,
                    RequestsType, Profile, Enabled, SetModuleStateRequest,
                    EvalScriptMockRequest, EvalCronScriptRequest, Script,
                    ChangeDeviceRequest)
import typer

app = typer.Typer(name=__app_name__)
app.add_typer(config_app)

config_dict = read_config()
SURGE_HTTP_API_ENDPOINT = config_dict["SURGE_HTTP_API_ENDPOINT"]
SURGE_HTTP_API_KEY = config_dict["SURGE_HTTP_API_KEY"]
# CRED_DICT = {
#     'endpoint': SURGE_HTTP_API_ENDPOINT,
#     'api_key': SURGE_HTTP_API_KEY
# }


@app.command('cap')
def get_set_cap(capability: Capability, on_off: OnOffEnum | None = typer.Argument(None)):
	"""
	Get or set a capability.
	"""
	client = SurgeAPIClient(SURGE_HTTP_API_ENDPOINT, SURGE_HTTP_API_KEY)
	if on_off is None:
		print(client.get_cap(capability))
	else:
		print(client.set_cap(capability, strtobool(on_off)))



if __name__ == '__main__':
	app()
