import pickle
from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.table import Table

DATE_FORMAT = "%d.%m.%Y"
BOOK_FILE_PATH = Path(__file__).resolve().parent / "files/addressbook.pkl"

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


def create_table(title, columns, rows, markup=False):
    console = Console()
    table = Table(title=title, show_header=True, header_style="bold cyan")

    for col in columns:
        table.add_column(
            col.get("name", ""),
            style=col.get("style", "white"),
            width=col.get("width", None)
        )

    for row in rows:
        table.add_row(*row)

    console.print(table, markup=markup)


def save_data(book, path=BOOK_FILE_PATH):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(book, f)
    except (IOError, OSError):
        print(f"Can`t save data in file {path}")


def load_data(path=BOOK_FILE_PATH):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"File {path} not found, a new book has been created")
        return AddressBook()
    except (pickle.UnpicklingError, EOFError, AttributeError):
        print(f"File {path} is corrupted, a new book has been created")
    except Exception:
        print(f"Can`t load data from file {path}")
        return AddressBook()


# TODO: Need specification for this feature
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"ValueError: {e}")
        except AttributeError:
            print("Error: Contact not found.")
        except Exception as e:
            print(f"Error: {e}")

    return wrapper


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"Number must be 10 digits long and contain only digits. Current length: {len(value)}")
        super().__init__(value)

    def validate(self, phone):
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    def __init__(self, value):
        date = self.validateDate(value)
        super().__init__(date)

    def validateDate(self, value):
        try:
            date = datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        if date > datetime.now():
            raise ValueError("Birth date cannot be in the future")

        if (datetime.now().year - date.year) > 100:
            raise ValueError("Age cannot exceed 100 years")

        return date


# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)

        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)

        if not phone_obj:
            raise ValueError(f"Phone {old_phone} does not exist.")

        index = self.phones.index(phone_obj)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        phone = filter(lambda p: p.value == phone, self.phones)
        return next(phone, None)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        birthdays = []

        for user_data in self.data.values():
            if not user_data.birthday or not user_data.birthday.value:
                continue

            birthday = user_data.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if birthday_this_year >= today and birthday_this_year < next_week:
                if birthday_this_year.weekday() in (5, 6):
                    birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

                birthdays.append(
                    {
                        "name": user_data.name.value,
                        "congratulation_date": birthday_this_year.strftime(DATE_FORMAT),
                    }
                )

        return birthdays


@input_error
# add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним
# номером, або телефонний номер к контакту який вже існує.
def add(args, book):
    if len(args) < 2:
        return "Error: Please provide contact name and phone number."

    name, phone = args
    record = book.find(name)
    message = "Contact updated."

    if not record:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)
    return message


@input_error
# change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
def change(args, book):
    if len(args) < 3:
        return "Error: Please provide contact name, old phone, and new phone."

    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)

    return f"Phone number for {name} changed from {old_phone} to {new_phone}."


@input_error
# phone [ім'я]: Показати телефонні номери для вказаного контакту.
def phone(args, book):
    if len(args) < 1:
        return "Error: Please provide contact name."

    name = args[0]
    record = book.find(name)
    phones = ", ".join(p.value for p in record.phones)

    if not phones:
        return f"Contact {name} has no phone numbers."

    return f"Phone numbers for {name}: {phones}"


@input_error
# all: Показати всі контакти в адресній книзі.
def all(_, book):
    if not book.data:
        return "No contacts in address book."

    rows = []
    for record in book.data.values():
        phones = ", ".join(phone.value for phone in record.phones)
        birthday = record.birthday.value.strftime(DATE_FORMAT) if record.birthday else "-"
        rows.append([record.name.value, phones, birthday])

    create_table("All Contacts", CONTACTS_COLUMNS, rows)
    return ""


@input_error
# add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
def add_birthday(args, book):
    if len(args) < 2:
        return "Error: Please provide contact name and birthday."

    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)

    return f"Birthday for {name} added successfully."


@input_error
# show-birthday [ім'я]: Показати дату народження для вказаного контакту.
def show_birthday(args, book):
    if len(args) < 1:
        return "Error: Please provide contact name."

    name = args[0]
    # we can not use dict as variable name because it is built-in type
    record = book.find(name)

    if not record.birthday:
        return f"{name} has no birthday set."

    return f"{name}'s birthday: {record.birthday.value.strftime(DATE_FORMAT)}"


@input_error
# birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
def birthdays(_, book):
    upcoming_birthdays = book.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."

    rows = [[b['name'], b['congratulation_date']] for b in upcoming_birthdays]

    create_table("Upcoming Birthdays (Next 7 Days)", BIRTHDAYS_COLUMNS, rows)
    return ""


# hello: Отримати вітання від бота.
def hello(_, __):
    return "Hello! How can I help you?"


def show_help(_, __):
    rows = [
        ["add", "[name] [phone]", "Add new contact"],
        ["change", "[name] [old] [new]", "Change phone number"],
        ["phone", "[name]", "Show phone number"],
        ["all | list", "", "Show all contacts"],
        ["add-birthday | add-b", "[name] [DD.MM.YYYY]", "Add birthday"],
        ["show-birthday", "[name]", "Show birthday"],
        ["birthdays", "", "Upcoming birthdays (7 days)"],
        ["exit | close", "", "Exit program"]
    ]

    create_table("Available Commands", HELP_COLUMNS, rows, markup=False)
    return ""


commands = {
    "add": add,
    "change": change,
    "phone": phone,
    "all": all,
    "list": all,
    "show-birthday": show_birthday,
    "add-b": add_birthday,
    "birthdays": birthdays,
    "hi": hello,
    "hello": hello,
    "help": show_help,
}

custom_style = Style.from_dict({
    '': '#ffff00 bold',
    'completion-menu': 'bg:#0000aa #ffffff',
    'completion-menu.completion': 'bg:#0000aa #cccccc',
    'completion-menu.completion.current': 'bg:#00aaaa #000000 bold',
})


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    command_completer = WordCompleter(
        list(commands.keys()) + ["close", "exit"],
        ignore_case=True,
        sentence=True
    )

    session = PromptSession(
        completer=command_completer,
        style=custom_style
    )

    try:
        while True:
            try:
                user_input = session.prompt("Enter command: ")
            except (EOFError, KeyboardInterrupt):
                print("\nProgram finished.\n -Have a good day user! ©Tron.\n")
                break

            if not user_input.strip():
                print("Please enter a command user (write help for more info).")
                continue

            command, *args = user_input.split()
            command = command.strip().lower()

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command in commands:
                print(commands[command](args, book))

            else:
                print("Invalid command.")

    finally:
        save_data(book=book)


if __name__ == "__main__":
    main()
