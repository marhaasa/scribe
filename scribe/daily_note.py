import typer
from rich import print
import subprocess
from scribe.utils import format_date
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
            print(f"Creating new daily note: {TODAY_NOTE_PATH}")
            TODAY_NOTE_PATH.write_text(format_daily_note_content())
        else:
            print(f"Daily note already exists: {TODAY_NOTE_PATH}")
    except IOError as e:
        print(f"An error occurred when creating daily note: {e}")


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
    except IOError as e:
        print(f"A problem occurred when adding note to daily note: {e}")


def open_daily_note() -> None:
    """
    Opens today's daily note in Neovim.
    Creates the note if it doesn't exist before opening.
    """

    # TODO: use the function from utils
    create_daily_note()
    try:
        subprocess.run(
            ["nvim", "+ normal Gzzo", str(TODAY_NOTE_PATH), "-c", ":NoNeckPain"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"A problem occurred when opening daily note in Neovim: {e}")
