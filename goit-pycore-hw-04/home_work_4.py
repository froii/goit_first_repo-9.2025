import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "path/to/phone_book.txt"

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

def add_contact(args, contacts): 
    try:
        name, phone = args
    except ValueError:
        return "Error: provide name and phone separated by space."
    
    contacts[name] = phone

    return "Contact added."

def change_contact(args, contacts):
    try:
        name, phone = args
    except ValueError:
        return "Error: provide name and phone separated by space."
    
    if name not in contacts:
        return "Error: contact not found."
    
    contacts[name] = phone
    return "Contact updated."

def get_phone(args, contacts):
    if not args:
        return "Error: provide a name."
    name = args[0]
    return contacts.get(name, "Contact not found.")

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

# Критерії оцінювання:

# Бот повинен перебувати в нескінченному циклі, чекаючи команди користувача.
# Бот завершує свою роботу, якщо зустрічає слова: "close" або "exit".
# Бот не чутливий до регістру введених команд.

# Бот приймає команди:
# "hello", та відповідає у консоль повідомленням "How can I help you?"
# "add username phone". За цією командою бот зберігає у пам'яті, наприклад у словнику, новий контакт. Користувач вводить ім'я username та номер телефону phone, обов'язково через пробіл.
# "close", "exit" за будь-якою з цих команд бот завершує свою роботу після того, як виведе у консоль повідомлення "Good bye!" та завершить своє виконання.

# "change username phone". За цією командою бот зберігає в пам'яті новий номер телефону phone для контакту username, що вже існує в записнику.
# "phone username" За цією командою бот виводить у консоль номер телефону для зазначеного контакту username.
# "all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.

# Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків та повертають рядок.
# Вся логіка взаємодії з користувачем реалізована у функції main, всі print та input відбуваються тільки там.