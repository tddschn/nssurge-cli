from . import __version__, __app_name__
import typer

app = typer.Typer(name=__app_name__)

if __name__ == '__main__':
    app()
