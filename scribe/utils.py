import subprocess
from rich import print
from scribe.config import EDITOR_COMMAND
from datetime import datetime, timedelta


def format_date(delta_days=0):
    return (datetime.now() + timedelta(days=delta_days)).strftime("%Y-%m-%d")


def open_in_editor(file_path: str, use_noneckpain: bool = False) -> None:
    """Open the created file in the configured editor.
    
    Args:
        file_path: Path to the file to open
        use_noneckpain: Whether to use NoNeckPain plugin and cursor positioning for notes
    """
    try:
        if use_noneckpain and EDITOR_COMMAND == "nvim":
            # Enhanced Neovim opening for notes - positions cursor and activates NoNeckPain
            subprocess.run(
                ["nvim", "+ normal Gzzo", str(file_path), "-c", ":NoNeckPain"],
                check=True,
            )
        else:
            # Standard editor opening
            subprocess.run([EDITOR_COMMAND, file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to open '{file_path}' with {EDITOR_COMMAND}. Exit code: {e.returncode}")
        print("This might be due to editor configuration issues or the file being locked.")
    except FileNotFoundError:
        print(f"Error: {EDITOR_COMMAND} command not found.")
        print(f"Please install {EDITOR_COMMAND} or update your PATH environment variable.")
        print("You can also set a different editor in scribe/config.py")
