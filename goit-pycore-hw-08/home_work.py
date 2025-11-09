import pickle
from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path

DATE_FORMAT = "%d.%m.%Y"
BOOK_FILE_PATH = Path(__file__).resolve().parent / "files/addressbook.pkl"

# Реалізуйте функціонал для збереження стану AddressBook у файл при
# закритті програми та відновлення стану при її запуску.

# Критерії оцінювання:
# Реалізовано протокол серіалізації / десеріалізації даних за допомогою pickle.
# Усі дані повинні зберігатися при виході з програми.
# При новому сеансі адресна книга, яка була при попередньому запуску, повинна бути в застосунку.


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

    result = []
    for record in book.data.values():
        phones = ", ".join(phone.value for phone in record.phones)
        birthday = f"; birthday: {record.birthday.value.strftime(DATE_FORMAT)}" if record.birthday else ""
        result.append(f"Contact name: {record.name.value}; phones: {phones} {birthday}")

    return "\n".join(result)


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

    return "Upcoming birthdays:\n" + "\n".join(f"{b['name']}:{b['congratulation_date']}" for b in upcoming_birthdays)


# hello: Отримати вітання від бота.
def hello(_, __):
    return "Hello! How can I help you?"


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    try:
        commands = {
            "add": add,
            "change": change,
            "phone": phone,
            "all": all,
            "add-birthday": add_birthday,
            "show-birthday": show_birthday,
            "birthdays": birthdays,
            "hello": hello,
        }

        while True:
            user_input = input("Enter a command: ")
            if not user_input.strip():
                print("Please enter a command.")
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

    except KeyboardInterrupt:
        print("\nProgram finished.\n -Have a good day user! ©Tron.")
    finally:
        save_data(book=book)


if __name__ == "__main__":
    main()
