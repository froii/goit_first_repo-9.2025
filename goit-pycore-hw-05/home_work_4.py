import json
import os
from pathlib import Path
from functools import wraps
from datetime import datetime

DATA_FILE = Path(__file__).resolve().parent / "path/to/phone_book.txt"


# Критерії оцінювання:
# Наявність декоратора input_error, який обробляє помилки введення користувача для всіх команд.
# Обробка помилок типу KeyError, ValueError, IndexError у функціях за допомогою декоратора input_error.
# Кожна функція для обробки команд має декоратор input_error, який обробляє відповідні помилки і 
# повертає відповідні повідомлення про помилку.
# Коректна реакція бота на різні команди та обробка помилок введення без завершення програми.

def write_log(message, filename='errors.log'):
    log_file = Path(__file__).resolve().parent / filename
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

# якщо зрозумів правильно, то є тільки 1 текст для всіх помилок. 
# в завдані є тільки одна помилка, хоча я згоден - одна помилка для всіх логів це погана ідея, але ж так написано )
def decorator_input_error(level="INFO"):
    def input_error(func):
        @wraps(func)
        def inner(*args, **kwargs):
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            main_logger_part = f"{date} {level} In function {func.__name__} -"

            try:
                return func(*args, **kwargs)
            except KeyError:
                message = f"{main_logger_part} Contact not found. Use 'add <name> <phone>' to create it first."
                write_log(message)
                return message
            except ValueError:
                message = f"{main_logger_part} Please provide both a name and a phone number."
                write_log(message)
                return message
            except IndexError:
                message = f"{main_logger_part} Please specify the contact name after the command."
                write_log(message)
                return message
        return inner
    return input_error


def load_contacts(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_contacts(filename, contacts):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.lower(), args

@decorator_input_error('ERROR')
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@decorator_input_error('WARNING')
def change_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact updated."

@decorator_input_error()
def get_phone(args, contacts):
    name = args[0]
    return contacts[name]

def get_all_contacts(contacts):
    if not contacts:
        return "No contacts found."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return '\n'.join(lines)

# Main function 
def main():
    contacts = load_contacts(DATA_FILE)
    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ")
            if user_input == "":
                print("No command entered.")
                continue

            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_contacts(DATA_FILE, contacts)
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, contacts))
            elif command == "change":
                print(change_contact(args, contacts))
            elif command == "phone":
                print(get_phone(args, contacts))
            elif command == "all":
                print(get_all_contacts(contacts))
            else:
                print("Invalid command.")
                
    except KeyboardInterrupt:
        save_contacts(DATA_FILE, contacts)
        print("\nGood bye!")


def initialize_data_file(filename):
    filename.parent.mkdir(parents=True, exist_ok=True)
    if not filename.exists():
        filename.write_text("{}", encoding="utf-8")

if __name__ == "__main__":
    initialize_data_file(DATA_FILE)
    main()
