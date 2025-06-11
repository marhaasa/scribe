import typer
from rich import print
from scribe.utils import format_date, open_in_editor
from scribe.config import NOTES_ROOT

app = typer.Typer()

TODAY = format_date()
YESTERDAY = format_date(-1)
TOMORROW = format_date(1)
DAILY_NOTES_PATH = NOTES_ROOT / "periodic-notes" / "daily-notes"
TODAY_NOTE_PATH = DAILY_NOTES_PATH / f"{TODAY}.md"


def format_daily_note_content() -> str:
    """
    Creates the daily note template content.

    Returns:
        str: Formatted content for the daily note.
    """
    # TODO: Consider moving this template to a separate config file
    return f"""
[[{YESTERDAY}]] - [[{TOMORROW}]]

## Daily rituals

- [ ] Drink water
- [ ] Walk the dog
- [ ] Exercise
- [ ] Read
- [ ] Tidy up

## Journal

"""


def create_daily_note() -> None:
    """
    Creates the daily note if it doesn't exist.
    If the note already exists, it prints a message indicating so.
    """
    try:
        if not TODAY_NOTE_PATH.exists():
            # Ensure parent directory exists
            DAILY_NOTES_PATH.mkdir(parents=True, exist_ok=True)
            TODAY_NOTE_PATH.write_text(format_daily_note_content())
            print(f"Created daily note: {TODAY_NOTE_PATH}")
        else:
            print(f"Daily note already exists: {TODAY_NOTE_PATH}")
    except PermissionError:
        print(f"Error: Permission denied when creating daily note at {TODAY_NOTE_PATH}")
        print("Check that you have write permissions to your notes directory.")
    except OSError as e:
        print(f"Error: Could not create daily note at {TODAY_NOTE_PATH}")
        print(f"System error: {e}")
        print("Check that your NOTES environment variable points to a valid directory.")


def append_daily_note(note_title: str) -> None:
    """
    Appends given note title to daily note as Obsidian markdown link.

    Args:
        note_title (str): The title of the note to be appended.
    """
    create_daily_note()
    try:
        with TODAY_NOTE_PATH.open(mode="a") as note:
            note.write(f"\n[[{note_title}]]")
    except PermissionError:
        print(f"Error: Permission denied when updating daily note at {TODAY_NOTE_PATH}")
        print("Check that you have write permissions to your notes directory.")
    except OSError as e:
        print(f"Error: Could not update daily note at {TODAY_NOTE_PATH}")
        print(f"System error: {e}")
        print("The daily note file may be locked or corrupted.")


def open_daily_note() -> None:
    """
    Opens today's daily note in the configured editor.
    Creates the note if it doesn't exist before opening.
    """
    create_daily_note()
    open_in_editor(str(TODAY_NOTE_PATH), use_noneckpain=True)
