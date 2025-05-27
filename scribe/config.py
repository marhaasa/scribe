from pathlib import Path
import os
import sys

def validate_environment():
    """Validate required environment variables and paths."""
    notes_path = os.environ.get("NOTES")
    if not notes_path:
        print("Error: NOTES environment variable is required.")
        print("Please set NOTES to your notes directory path.")
        print("Example: export NOTES=/path/to/your/notes")
        sys.exit(1)
    
    notes_root = Path(notes_path)
    if not notes_root.exists():
        print(f"Error: Notes directory does not exist: {notes_path}")
        print("Please create the directory or update the NOTES environment variable.")
        sys.exit(1)
    
    return notes_root

# Validate environment on import
NOTES_ROOT = validate_environment()

# Paths
INBOX_PATH = NOTES_ROOT / "0-inbox"

# File settings
MAX_TITLE_LENGTH = 80

# Prompts
PROMPT_TITLE = "Enter note title"

# Commands
EDITOR_COMMAND = "nvim"
