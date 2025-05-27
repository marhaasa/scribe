import typer

from scribe import new_note
from scribe import daily_note
from scribe import __version__

from typing import Optional
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def new(
    title: Annotated[Optional[str], typer.Argument()] = None,
    vim_mode: Annotated[bool, typer.Option("--vim")] = False,
) -> None:
    """Create a new note with the given title. If no title is provided, it will be prompted.
    Adds links to today's note.
    """
    new_note.create_new_note(title, vim_mode)


@app.command()
def daily():
    """Open today's note. Creates a new one if it doesn't exist."""
    daily_note.open_daily_note()


@app.command()
def version():
    """Show the version of the CLI."""
    typer.echo(f"scribe version {__version__}")
