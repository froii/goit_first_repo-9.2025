import re
from collections import UserDict
from datetime import datetime, timedelta

DATE_FORMAT = "%d.%m.%Y"


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Номер телефону повинен містити рівно 10 цифр")
        super().__init__(value)

    def validate(self, phone):
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    def __init__(self, value):
        try:
            if self.validate(value):
                # та перетворіть рядок на об'єкт datetime
                date = datetime.strptime(value, DATE_FORMAT)
                super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    # Додайте перевірку коректності даних
    def validate(self, date):
        return re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", date) is not None


# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
# Додавання телефонів
# Видалення телефонів
# Редагування телефонів
# Пошук телефону


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
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    # Це поле не обов'язкове, але може бути тільки одне. - це значить що воно не мутабельне чи просто одне і оновлюється?
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


# AddressBook: Клас для зберігання та управління записами.
# Додавання записів
# Пошук записів за іменем
# Видалення записів за іменем


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Додайте та адаптуйте до класу AddressBook нашу функцію з четвертого домашнього завдання, тиждень 3, get_upcoming_birthdays,
    # яка для контактів адресної книги повертає список користувачів, яких потрібно привітати по днях на наступному тижні.
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
                    birthday_this_year += timedelta(
                        days=(7 - birthday_this_year.weekday())
                    )

                birthdays.append(
                    {
                        "name": user_data.name.value,
                        "congratulation_date": birthday_this_year.strftime(DATE_FORMAT),
                    }
                )

        return birthdays


# Опис задачі:
# Розробіть систему для управління адресною книгою.


# Command handlers
def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.lower(), args


def add_contact(args, book):
    if len(args) < 2:
        return "Error: Please provide both name and phone number."

    name, phone = args[0], args[1]

    try:
        record = book.find(name)
        if record:
            record.add_phone(phone)
            return f"Phone {phone} added to existing contact {name}."
        else:
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            return f"Contact {name} added with phone {phone}."
    except ValueError as e:
        return f"Error: {str(e)}"


def change_contact(args, book):
    if len(args) < 3:
        return "Error: Please provide name, old phone, and new phone."

    name, old_phone, new_phone = args[0], args[1], args[2]

    record = book.find(name)
    if not record:
        return f"Error: Contact {name} not found."

    try:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {name} changed from {old_phone} to {new_phone}."
    except ValueError as e:
        return f"Error: {str(e)}"


def show_phone(args, book):
    if len(args) < 1:
        return "Error: Please provide contact name."

    name = args[0]
    record = book.find(name)

    if not record:
        return f"Error: Contact {name} not found."

    if not record.phones:
        return f"{name} has no phone numbers."

    phones = ", ".join(phone.value for phone in record.phones)
    return f"{name}: {phones}"


def show_all(book):
    if not book.data:
        return "No contacts in address book."

    lines = [str(record) for record in book.data.values()]
    return "\n".join(lines)


def add_birthday(args, book):
    if len(args) < 2:
        return "Error: Please provide name and birthday (DD.MM.YYYY)."

    name, birthday = args[0], args[1]

    record = book.find(name)
    if not record:
        return f"Error: Contact {name} not found."

    try:
        record.add_birthday(birthday)
        return f"Birthday {birthday} added for {name}."
    except ValueError as e:
        return f"Error: {str(e)}"


def show_birthday(args, book):
    if len(args) < 1:
        return "Error: Please provide contact name."

    name = args[0]
    record = book.find(name)

    if not record:
        return f"Error: Contact {name} not found."

    if not record.birthday:
        return f"{name} has no birthday set."

    return f"{name}'s birthday: {record.birthday.value.strftime(DATE_FORMAT)}"


def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays in the next week."

    lines = [f"{item['name']}: {item['congratulation_date']}" for item in upcoming]
    return "Upcoming birthdays:\n" + "\n".join(lines)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
