import typer
from rich import print
from datetime import datetime
from pathlib import Path
from scribe.utils import format_date, open_in_editor
from scribe.config import NOTES_ROOT, LANGUAGE, GROUPS_FILE
from scribe.daily_note import append_daily_note
from typing import Optional
import re
import tomllib

app = typer.Typer()

TODAY = format_date()
MEETING_NOTES_PATH = NOTES_ROOT / "0-inbox"

MEETING_TEMPLATES = {
    "en": {
        "general": {
            "name": "General Meeting",
            "template": """## Participants

- [ ] 
- [ ] 
- [ ] 

## Agenda

- 

## Notes

## Action Items

- [ ] 
- [ ] 

## Next Steps

"""
        },
        "standup": {
            "name": "Daily Standup",
            "template": """## Team Members

- [ ] 
- [ ] 
- [ ] 

## Yesterday's Progress

## Today's Plan

## Blockers

## Notes

"""
        },
        "1on1": {
            "name": "1-on-1 Meeting",
            "template": """## Participants

- [ ] 
- [ ] 

## How are you doing?

## Current Projects

## Challenges & Support Needed

## Career Development

## Feedback

## Action Items

- [ ] 
- [ ] 

"""
        },
        "retrospective": {
            "name": "Sprint Retrospective",
            "template": """## What went well?

- 

## What could be improved?

- 

## What will we try next?

- 

## Action Items

- [ ] 
- [ ] 

"""
        }
    },
    "no": {
        "general": {
            "name": "Møte",
            "template": """## Deltakere

- [ ] 
- [ ] 
- [ ] 

## Agenda

- 

## Notater

## Oppgaver

- [ ] 
- [ ] 

## Neste Steg

"""
        },
        "standup": {
            "name": "Daglig Standup",
            "template": """## Gruppemedlemmer

- [ ] 
- [ ] 
- [ ] 

## Gårsdagens fremgang

## Dagens plan

## Hindringer

## Notater

"""
        },
        "1on1": {
            "name": "1-til-1 Møte",
            "template": """## Deltakere

- [ ] 
- [ ] 

## Hvordan har du det?

## Nåværende prosjekter

## Utfordringer og behov

## Karriereutvikling

## Tilbakemelding

## Oppgaver

- [ ] 
- [ ] 

"""
        },
        "retrospective": {
            "name": "Sprint Retrospektiv",
            "template": """## Hva gikk bra?

- 

## Hva kan forbedres?

- 

## Hva skal vi prøve neste gang?

- 

## Oppgaver

- [ ] 
- [ ] 

"""
        }
    }
}


def load_group(group_name: str) -> list[str]:
    """Load a named group of members from the groups config file."""
    if not GROUPS_FILE.exists():
        print(f"[red]Error:[/red] Groups file not found: {GROUPS_FILE}")
        print(f"Create it with a [groups] section, e.g.:")
        print(f'  [groups]\n  {group_name} = ["Alice", "Bob"]')
        raise typer.Exit(code=1)

    with open(GROUPS_FILE, "rb") as f:
        config = tomllib.load(f)

    groups = config.get("groups", {})
    if group_name not in groups:
        print(f"[red]Error:[/red] Group '{group_name}' not found in {GROUPS_FILE}")
        if groups:
            print("Available groups:")
            for name in groups:
                print(f"  {name}: {', '.join(groups[name])}")
        raise typer.Exit(code=1)

    return groups[group_name]


def _inject_members(template: str, members: list[str]) -> str:
    """Replace empty participant/member checkbox lines with actual member names."""
    member_lines = "\n".join(f"- [ ] {name}" for name in members) + "\n"
    # Replace only the first block of empty checkboxes (participants section)
    return re.sub(r"(- \[ \] *\n)+", member_lines, template, count=1)


def format_meeting_note_content(template_key: str = "general", members: Optional[list[str]] = None) -> str:
    """
    Creates meeting note template content based on template type.

    Args:
        template_key: The type of meeting template to use
        members: Optional list of participant names to inject

    Returns:
        str: Formatted content for the meeting note.
    """
    lang_templates = MEETING_TEMPLATES.get(LANGUAGE, MEETING_TEMPLATES["en"])
    template = lang_templates.get(template_key, lang_templates["general"])
    content = template["template"]
    if members:
        content = _inject_members(content, members)
    return content


def generate_meeting_filename(title: Optional[str] = None, template_key: str = "general") -> str:
    """
    Generate a filename for the meeting note.
    
    Args:
        title: Optional custom title for the meeting
        template_key: The template type being used
        
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    if title:
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_title = clean_title.replace(' ', '-')
        return f"{timestamp}-{clean_title}.md"
    else:
        lang_templates = MEETING_TEMPLATES.get(LANGUAGE, MEETING_TEMPLATES["en"])
        template_name = lang_templates[template_key]["name"].replace(' ', '-').lower()
        return f"{timestamp}-{template_name}.md"


def create_meeting_note(title: Optional[str] = None, template_key: str = "general", members: Optional[list[str]] = None) -> Path:
    """
    Creates a meeting note with the specified template.

    Args:
        title: Optional title for the meeting
        template_key: The type of meeting template to use
        members: Optional list of participant names

    Returns:
        Path: Path to the created meeting note
    """
    filename = generate_meeting_filename(title, template_key)
    meeting_note_path = MEETING_NOTES_PATH / filename

    try:
        if not meeting_note_path.exists():
            # Ensure parent directory exists
            MEETING_NOTES_PATH.mkdir(parents=True, exist_ok=True)

            lang_templates = MEETING_TEMPLATES.get(LANGUAGE, MEETING_TEMPLATES["en"])
            note_title = title or f"{lang_templates[template_key]['name']} - {TODAY}"
            content = f"# {note_title}\n\n{format_meeting_note_content(template_key, members)}"
            meeting_note_path.write_text(content)
            
            # Add meeting note to daily note (same as regular notes)
            append_daily_note(meeting_note_path.stem)  # Use filename without .md extension
            
            print(f"Created meeting note: {meeting_note_path}")
        else:
            print(f"Meeting note already exists: {meeting_note_path}")
        return meeting_note_path
    except PermissionError:
        print(f"Error: Permission denied when creating meeting note at {meeting_note_path}")
        print("Check that you have write permissions to your notes directory.")
        raise
    except OSError as e:
        print(f"Error: Could not create meeting note at {meeting_note_path}")
        print(f"System error: {e}")
        print("Check that your NOTES environment variable points to a valid directory.")
        raise


def list_available_templates() -> None:
    """List all available meeting templates."""
    print("Available meeting templates:")
    lang_templates = MEETING_TEMPLATES.get(LANGUAGE, MEETING_TEMPLATES["en"])
    for key, template in lang_templates.items():
        print(f"  {key}: {template['name']}")


def open_meeting_note(title: Optional[str] = None, template_key: str = "general", members: Optional[list[str]] = None) -> None:
    """
    Creates and opens a meeting note in the configured editor.

    Args:
        title: Optional title for the meeting
        template_key: The type of meeting template to use
        members: Optional list of participant names
    """
    meeting_note_path = create_meeting_note(title, template_key, members)
    open_in_editor(str(meeting_note_path), use_noneckpain=True)
