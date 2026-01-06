import typer

from scribe import new_note
from scribe import daily_note
from scribe import meeting_note
from scribe.config import LANGUAGE
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
def daily(
    no_edit: Annotated[bool, typer.Option("--no-edit", help="Create daily note without opening editor")] = False,
):
    """Open today's note. Creates a new one if it doesn't exist."""
    if no_edit:
        daily_note.create_daily_note()
    else:
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
    lang_templates = meeting_note.MEETING_TEMPLATES.get(LANGUAGE, meeting_note.MEETING_TEMPLATES["en"])
    if template not in lang_templates:
        typer.echo(f"Invalid template: '{template}' is not a valid meeting template.", err=True)
        typer.echo("Available templates:", err=True)
        for key, tmpl in lang_templates.items():
            typer.echo(f"  {key}: {tmpl['name']}", err=True)
        typer.echo("Use 'scribe meeting --list' for more details.", err=True)
        raise typer.Exit(code=1)
    
    meeting_note.open_meeting_note(title, template)


@app.command()
def version():
    """Show the version of the CLI."""
    typer.echo(f"scribe version {__version__}")
