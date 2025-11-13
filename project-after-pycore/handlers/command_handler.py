"""Command handler for processing user commands."""
from models import Record, AddressBook
from ui.table_renderer import TableRenderer
from constants import CONTACTS_COLUMNS, BIRTHDAYS_COLUMNS, HELP_COLUMNS
from .decorators import input_error


class CommandHandler:
    def __init__(self, address_book: AddressBook):
        self.book = address_book
        self.table_renderer = TableRenderer()
        self.commands = {
            "add": self.add,
            "change": self.change,
            "phone": self.phone,
            "delete": self.delete_contact,
            "remove": self.delete_contact,
            "delete-phone": self.delete_phone,
            "remove-phone": self.delete_phone,
            "edit-name": self.edit_name,
            "rename": self.edit_name,
            "all": self.all_contacts,
            "list": self.all_contacts,
            "show-birthday": self.show_birthday,
            "add-birthday": self.add_birthday,
            "add-b": self.add_birthday,
            "birthdays": self.birthdays,
            "hi": self.hello,
            "hello": self.hello,
            "help": self.show_help,
        }

    def get_command_names(self) -> list[str]:
        """Get list of all available command names."""
        return list(self.commands.keys())

    def execute(self, command: str, args: list[str]) -> str:
        """Execute a command with given arguments."""
        if command in self.commands:
            return self.commands[command](args)
        return "Invalid command."

    @input_error
    def add(self, args: list[str]) -> str:
        """Add a new contact or phone to existing contact."""
        if len(args) < 2:
            return "Error: Please provide contact name and phone number."

        name, phone = args
        record = self.book.find(name)
        message = "Contact updated."

        if not record:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."

        record.add_phone(phone)
        return message

    @input_error
    def change(self, args: list[str]) -> str:
        """Change phone number for a contact."""
        if len(args) < 3:
            return "Error: Please provide contact name, old phone, and new phone."

        name, old_phone, new_phone = args
        record = self.book.find(name)
        record.edit_phone(old_phone, new_phone)

        return f"Phone number for {name} changed from {old_phone} to {new_phone}."

    @input_error
    def phone(self, args: list[str]) -> str:
        """Show phone numbers for a contact."""
        if len(args) < 1:
            return "Error: Please provide contact name."

        name = args[0]
        record = self.book.find(name)
        phones = ", ".join(p.value for p in record.phones)

        if not phones:
            return f"Contact {name} has no phone numbers."

        return f"Phone numbers for {name}: {phones}"

    @input_error
    def delete_contact(self, args: list[str]) -> str:
        """Delete a contact from the address book."""
        if len(args) < 1:
            return "Error: Please provide contact name."

        name = args[0]
        record = self.book.find(name)

        if not record:
            return f"Contact {name} not found."

        self.book.delete(name)
        return f"Contact {name} deleted successfully."

    @input_error
    def delete_phone(self, args: list[str]) -> str:
        """Delete a phone number from a contact."""
        if len(args) < 2:
            return "Error: Please provide contact name and phone number."

        name, phone = args
        record = self.book.find(name)

        if not record:
            return f"Contact {name} not found."

        phone_obj = record.find_phone(phone)
        if not phone_obj:
            return f"Phone {phone} not found for contact {name}."

        record.remove_phone(phone)
        return f"Phone {phone} removed from contact {name}."

    @input_error
    def edit_name(self, args: list[str]) -> str:
        """Edit contact name."""
        if len(args) < 2:
            return "Error: Please provide old name and new name."

        old_name, new_name = args
        record = self.book.find(old_name)

        if not record:
            return f"Contact {old_name} not found."

        if self.book.find(new_name):
            return f"Contact {new_name} already exists."

        # Delete old record and add with new name
        self.book.delete(old_name)
        record.name.value = new_name
        self.book.add_record(record)

        return f"Contact name changed from {old_name} to {new_name}."

    @input_error
    def all_contacts(self, args: list[str]) -> str:
        """Show all contacts in the address book."""
        if not self.book.data:
            return "No contacts in address book."

        rows = []
        for record in self.book.data.values():
            phones = ", ".join(phone.value for phone in record.phones)
            birthday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "-"
            rows.append([record.name.value, phones, birthday])

        self.table_renderer.render("All Contacts", CONTACTS_COLUMNS, rows)
        return ""

    @input_error
    def add_birthday(self, args: list[str]) -> str:
        """Add birthday to a contact."""
        if len(args) < 2:
            return "Error: Please provide contact name and birthday."

        name, birthday = args
        record = self.book.find(name)
        record.add_birthday(birthday)

        return f"Birthday for {name} added successfully."

    @input_error
    def show_birthday(self, args: list[str]) -> str:
        """Show birthday for a contact."""
        if len(args) < 1:
            return "Error: Please provide contact name."

        name = args[0]
        record = self.book.find(name)

        if not record.birthday:
            return f"{name} has no birthday set."

        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"

    @input_error
    def birthdays(self, args: list[str]) -> str:
        """Show upcoming birthdays in the next 7 days."""
        upcoming_birthdays = self.book.get_upcoming_birthdays()

        if not upcoming_birthdays:
            return "No upcoming birthdays in the next week."

        rows = [[b['name'], b['congratulation_date']] for b in upcoming_birthdays]
        self.table_renderer.render("Upcoming Birthdays (Next 7 Days)", BIRTHDAYS_COLUMNS, rows)
        return ""

    def hello(self, args: list[str]) -> str:
        """Greet the user."""
        return "Hello! How can I help you?"

    def show_help(self, args: list[str]) -> str:
        """Show available commands."""
        rows = [
            ["add", "[name] [phone]", "Add new contact"],
            ["change", "[name] [old] [new]", "Change phone number"],
            ["phone", "[name]", "Show phone number"],
            ["delete | remove", "[name]", "Delete contact"],
            ["delete-phone", "[name] [phone]", "Delete phone from contact"],
            ["edit-name | rename", "[old] [new]", "Rename contact"],
            ["all | list", "", "Show all contacts"],
            ["add-birthday | add-b", "[name] [DD.MM.YYYY]", "Add birthday"],
            ["show-birthday", "[name]", "Show birthday"],
            ["birthdays", "", "Upcoming birthdays (7 days)"],
            ["exit | close", "", "Exit program"]
        ]

        self.table_renderer.render("Available Commands", HELP_COLUMNS, rows, markup=False)
        return ""
