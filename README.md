# Scribe

A CLI for managing notes in Neovim + Obsidian. Heavily inspired by [Zettelkasten CLI](https://github.com/mischavandenburg/zettelkasten-cli).

## Requirements

- Python 3.12+
- Neovim with NoNeckPain plugin (optional but recommended)
- NOTES environment variable set to your notes directory

## Configuration

**Required Environment Variables:**
- `NOTES`: Path to your notes directory

**Optional Environment Variables:**
- `SCRIBE_LANG`: Language for templates (default: `en`)
  - `en`: English templates
  - `no`: Norwegian templates

## Installation

```bash
# Set up your notes directory
export NOTES=/path/to/your/notes

# Optional: Set language preference (add to ~/.zshrc or ~/.bashrc for persistence)
export SCRIBE_LANG=no  # For Norwegian templates, or 'en' for English (default)

# Install via homebrew (coming soon)
brew tap marhaasa/tools
brew install marhaasa/tools/scribe
```

## Setup

Make sure your notes directory has the following structure:
```
$NOTES/
├── 0-inbox/
└── periodic-notes/
    └── daily-notes/
```

**Usage**:

```console
[OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `daily`: Open daily note or create if it doesn't exist.
- `meeting`: Create a meeting note with the specified template.
- `new`: Create a new note with the provided title.

## `daily`

Open daily note or create if it doesn't exist.

**Usage**:

```console
daily [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

## `meeting`

Create a meeting note with the specified template. Supports multiple meeting types with pre-defined templates.

**Usage**:

```console
meeting [OPTIONS] [TITLE]
```

**Arguments**:

- `[TITLE]`: Optional title for the meeting note

**Options**:

- `-t, --template TEXT`: Meeting template to use (default: general)
- `-l, --list`: List all available meeting templates
- `--help`: Show this message and exit.

**Available Templates**:

- `general`: General purpose meeting template
- `standup`: Daily standup meeting template  
- `1on1`: One-on-one meeting template
- `retrospective`: Sprint retrospective template

**Language Support**:
Templates are available in multiple languages based on the `SCRIBE_LANG` environment variable:
- English (`en`): Default templates
- Norwegian (`no`): Translated templates with Norwegian section headers

**Examples**:

```console
# Create a general meeting note
scribe meeting "Project Planning"

# Create a standup meeting note
scribe meeting --template standup

# List available templates
scribe meeting --list

# Use Norwegian templates
export SCRIBE_LANG=no
scribe meeting "Prosjektplanlegging"  # Creates Norwegian template
```

## `new`

Create a new note with the provided title. Will prompt if no title given.
Adds Obsidian markdown link to the daily note.

**Usage**:

```console
new [OPTIONS] [TITLE]
```

**Arguments**:

- `[TITLE]`

**Options**:

- `--vim`: Indicates input is coming from vim. Prevents new file being opened.
- `--help`: Show this message and exit.
