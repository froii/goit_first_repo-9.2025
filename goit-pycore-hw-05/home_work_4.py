import json
from pathlib import Path
from functools import wraps

DATA_FILE = Path(__file__).resolve().parent / "path/to/phone_book.txt"



# Критерії оцінювання:
# Наявність декоратора input_error, який обробляє помилки введення користувача для всіх команд.
# Обробка помилок типу KeyError, ValueError, IndexError у функціях за допомогою декоратора input_error.
# Кожна функція для обробки команд має декоратор input_error, який обробляє відповідні помилки і 
# повертає відповідні повідомлення про помилку.
# Коректна реакція бота на різні команди та обробка помилок введення без завершення програми.

#  якщо зрозумів правильно, то є тільки 1 текст для всіх помилок. 
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Enter the argument for the command"
    return inner




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

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."

@input_error
def get_phone(args, contacts):
    if not args:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError(name)
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
