from . import __version__, __app_name__, logger
from .config import app as config_app, get_creds
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
from nssurge_api import SurgeAPIClient
import typer

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

def _version_callback(value: bool) -> None:
	if value:
		typer.echo(f'{__app_name__} v{__version__}')
		raise typer.Exit()


@app.callback()
def main(version: bool = typer.Option(
	None,
	'--version',
	'-v',
	help='Show the application\'s version and exit.',
	callback=_version_callback,
	is_eager=True,
)):
	"""
	Surge CLI by Teddy Xinyuan Chen

	Command line tool for interacting with Surge's HTTP API
	and controlling Surge's behavior.

	Project homepage: https://github.com/tddschn/nssurge-cli
	
	Built with nssurge-api https://github.com/tddschn/nssurge-api

	Surge: https://nssurge.com

	Surge HTTP API: https://manual.nssurge.com/others/http-api.html
	"""





if __name__ == "__main__":
	app()
