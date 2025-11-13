"""Decorators for error handling."""


def input_error(func):
    """Decorator for handling input errors in command handlers."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except AttributeError:
            return "Error: Contact not found."
        except Exception as e:
            return f"Error: {e}"
    return wrapper
