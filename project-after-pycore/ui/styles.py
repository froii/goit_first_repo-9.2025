"""UI styles for the application."""
from prompt_toolkit.styles import Style


def get_prompt_style() -> Style:
    """Get the custom style for prompt_toolkit."""
    return Style.from_dict({
        '': '#ffff00 bold',
        'completion-menu': 'bg:#0000aa #ffffff',
        'completion-menu.completion': 'bg:#0000aa #cccccc',
        'completion-menu.completion.current': 'bg:#00aaaa #000000 bold',
    })
