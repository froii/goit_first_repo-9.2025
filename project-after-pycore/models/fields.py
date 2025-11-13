"""Field classes for contact information."""
from datetime import datetime
from constants import DATE_FORMAT


class Field:
    """Base class for all fields."""
    
    def __init__(self, value):
        self.value = value


class Name(Field):
    """Name field."""
    
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    """Phone field with validation."""
    
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(
                f"Number must be 10 digits long and contain only digits. "
                f"Current length: {len(value)}"
            )
        super().__init__(value)

    @staticmethod
    def validate(phone):
        """Validate phone number format."""
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    """Birthday field with validation."""
    
    def __init__(self, value):
        date = self.validate_date(value)
        super().__init__(date)

    @staticmethod
    def validate_date(value):
        """Validate birthday date."""
        try:
            date = datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        if date > datetime.now():
            raise ValueError("Birth date cannot be in the future")

        if (datetime.now().year - date.year) > 100:
            raise ValueError("Age cannot exceed 100 years")

        return date
