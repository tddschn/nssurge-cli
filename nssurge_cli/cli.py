from . import __version__, __app_name__
from .config import read_config
import typer

app = typer.Typer(name=__app_name__)

config_dict = read_config()
SURGE_HTTP_API_ENDPOINT = config_dict["SURGE_HTTP_API_ENDPOINT"]
SURGE_HTTP_API_KEY = config_dict["SURGE_HTTP_API_KEY"]
# CRED_DICT = {
#     'endpoint': SURGE_HTTP_API_ENDPOINT,
#     'api_key': SURGE_HTTP_API_KEY
# }



if __name__ == '__main__':
	app()
