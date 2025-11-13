"""Record class for storing contact information."""
from .fields import Name, Phone, Birthday


class Record:
    """Class for storing contact information including name, phones, and birthday."""
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """Add a phone number to the contact."""
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        """Remove a phone number from the contact."""
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        """Edit an existing phone number."""
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError(f"Phone {old_phone} does not exist.")
        
        index = self.phones.index(phone_obj)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        """Find a phone number in the contact."""
        phone_iter = filter(lambda p: p.value == phone, self.phones)
        return next(phone_iter, None)

    def add_birthday(self, birthday):
        """Add birthday to the contact."""
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"
