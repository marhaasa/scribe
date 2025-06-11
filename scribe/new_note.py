import typer
from rich import print
from typing import Optional
from pathlib import Path
from scribe.config import MAX_TITLE_LENGTH, INBOX_PATH, PROMPT_TITLE
from scribe.utils import open_in_editor
from scribe.daily_note import append_daily_note

app = typer.Typer()


def create_new_note(title, vim_mode) -> None:
    """Create a new note from the command line."""
    try:
        note_title = get_note_title(title)
        validate_title(note_title)
        file_path = format_path(note_title)
        create_file(file_path, note_title)
        if not vim_mode:
            open_in_editor(str(file_path))
    except ValueError as e:
        typer.echo(f"Invalid input: {str(e)}", err=True)
        typer.echo("Use 'scribe new --help' for usage information.", err=True)
        raise typer.Exit(code=1)
    except FileExistsError as e:
        typer.echo(f"File conflict: {str(e)}", err=True)
        typer.echo("Try a different title or check your notes directory.", err=True)
        raise typer.Exit(code=1)
    except PermissionError:
        typer.echo("Permission denied: Cannot create note in the specified directory.", err=True)
        typer.echo("Check that you have write permissions to your notes directory.", err=True)
        raise typer.Exit(code=1)
    except OSError as e:
        typer.echo(f"System error: Could not create note. {str(e)}", err=True)
        typer.echo("Check that your NOTES environment variable points to a valid directory.", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {str(e)}", err=True)
        typer.echo("Please report this issue if it persists.", err=True)
        raise typer.Exit(code=1)


def get_note_title(title: Optional[str]) -> str:
    """Get the note title from input or prompt the user."""
    return title.strip() if title else typer.prompt(PROMPT_TITLE)


def validate_title(title: str) -> None:
    """Validate the note title."""
    if not title:
        raise ValueError("Title cannot be empty.")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title cannot be longer than {MAX_TITLE_LENGTH} characters.")
    if title.endswith(".md"):
        raise ValueError("You don't need to include .md at the end.")


def format_path(note_title: str) -> Path:
    """Format the absolute path based on Zettelkasten location and the note title."""
    return INBOX_PATH / f"{note_title}.md"


def create_file(file_path: Path, note_title: str) -> None:
    """Create a new note file and open it in the editor."""
    if file_path.exists():
        raise FileExistsError(f"A note with this title already exists: {file_path.name}")
    
    try:
        # Ensure parent directory exists
        INBOX_PATH.mkdir(parents=True, exist_ok=True)
        create_note_file(file_path, note_title)
        print(f"Created note: {file_path.name}")
    except PermissionError:
        raise PermissionError(f"Cannot create note at {file_path}")
    except OSError as e:
        raise OSError(f"Failed to create note: {e}")


def create_note_file(file_path: Path, note_title: str) -> None:
    """
    Create a new note file with the given title, append the title to the daily note, and add a H1 Markdown heading.
    """
    try:
        append_daily_note(note_title)
        file_path.write_text(f"# {note_title}\n\n")
    except Exception as e:
        # Clean up partial file if daily note append failed
        if file_path.exists():
            file_path.unlink()
        raise
