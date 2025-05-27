# Scribe

A CLI for managing Zettelkasten notes in Neovim + Obsidian.

## Requirements

- Python 3.12+
- Neovim with NoNeckPain plugin (optional but recommended)
- NOTES environment variable set to your notes directory

## Installation

```bash
# Set up your notes directory
export NOTES=/path/to/your/notes

# Install via homebrew (coming soon)
brew tap yourusername/tap
brew install scribe
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
- `new`: Create a new note with the provided title.

## `daily`

Open daily note or create if it doesn't exist.

**Usage**:

```console
daily [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

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
