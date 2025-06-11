import typer

from scribe import new_note
from scribe import daily_note
from scribe import meeting_note
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
def meeting(
    title: Annotated[Optional[str], typer.Argument()] = None,
    template: Annotated[str, typer.Option("--template", "-t")] = "general",
    list_templates: Annotated[bool, typer.Option("--list", "-l")] = False,
) -> None:
    """Create a meeting note with the specified template."""
    if list_templates:
        meeting_note.list_available_templates()
        return
    
    # Validate template exists
    if template not in meeting_note.MEETING_TEMPLATES:
        typer.echo(f"Invalid template: '{template}' is not a valid meeting template.", err=True)
        typer.echo("Available templates:", err=True)
        for key, tmpl in meeting_note.MEETING_TEMPLATES.items():
            typer.echo(f"  {key}: {tmpl['name']}", err=True)
        typer.echo("Use 'scribe meeting --list' for more details.", err=True)
        raise typer.Exit(code=1)
    
    meeting_note.open_meeting_note(title, template)


@app.command()
def version():
    """Show the version of the CLI."""
    typer.echo(f"scribe version {__version__}")
