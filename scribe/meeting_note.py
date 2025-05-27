import typer
from rich import print
import subprocess
from scribe.utils import format_date
from scribe.config import NOTES_ROOT

app = typer.Typer()

TODAY = format_date()
MEETING_NOTES_PATH = NOTES_ROOT / "0-inbox"


def format_meeting_note_content() -> str:
    """
    Creates the daily note template content.

    Returns:
        str: Formatted content for the daily note.
    """
    # TODO: Consider moving this template to a separate config file
    return f"""


## Participants

- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 

## Journal

"""


def create_meeting_note() -> None:
    """
    Creates the meeting note.
    If the note already exists, it prints a message indicating so.
    """
    try:
        if not TODAY_NOTE_PATH.exists():
            print(f"Creating new meeting note: {TODAY_NOTE_PATH}")
            TODAY_NOTE_PATH.write_text(format_meeting_note_content())
        else:
            print(f"Meeting note already exists: {TODAY_NOTE_PATH}")
    except IOError as e:
        print(f"An error occurred when creating meeting note: {e}")


def open_meeting_note() -> None:
    """
    Opens today's daily note in Neovim.
    Creates the note if it doesn't exist before opening.
    """

    # TODO: use the function from utils
    create_meeting_note()
    try:
        subprocess.run(
            ["nvim", "+ normal Gzzo", str(TODAY_NOTE_PATH), "-c", ":NoNeckPain"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"A problem occurred when opening meeting note in Neovim: {e}")
