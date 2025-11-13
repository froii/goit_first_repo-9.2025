"""
Constants used throughout the application.

This module contains all constant values used in the assistant bot,
including date formats, file paths, and table column configurations.
"""
from pathlib import Path

# Date format for birthday display and input
DATE_FORMAT = "%d.%m.%Y"

# Default file path for address book storage (used as fallback)
BOOK_FILE_PATH = Path(__file__).resolve().parent / "files/addressbook.pkl"

# Table column configurations for Rich library
# Each column has: name (header), style (color), width (optional)

CONTACTS_COLUMNS = [
    {"name": "Name", "style": "green", "width": 20},
    {"name": "Phones", "style": "cyan", "width": 30},
    {"name": "Birthday", "style": "magenta", "width": 15}
]

BIRTHDAYS_COLUMNS = [
    {"name": "Name", "style": "green", "width": 20},
    {"name": "Congratulation Date", "style": "magenta", "width": 20}
]

HELP_COLUMNS = [
    {"name": "Command", "style": "green", "width": 30},
    {"name": "Arguments", "style": "cyan", "width": 20},
    {"name": "Description", "style": "white"}
]
