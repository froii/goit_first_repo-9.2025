import sys
from handlers import CommandHandler
from models import AddressBook
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from storage import StorageFactory
from ui import get_prompt_style


MODIFY_COMMANDS = {
    'add', 'change', 'delete', 'remove', 'delete-phone',
    'remove-phone', 'edit-name', 'rename', 'add-birthday', 'add-b'
}

class AssistantBot:
    def __init__(self, storage_type: str = 'pickle'):
        self.storage = StorageFactory.create_storage(storage_type)
        loaded_data = self.storage.load()

        if isinstance(loaded_data, AddressBook):
            self.book = loaded_data
        else:
            self.book = AddressBook()

        self.handler = CommandHandler(self.book)
        self.session = None

    def setup_prompt(self):
        command_completer = WordCompleter(
            self.handler.get_command_names() + ["close", "exit"],
            ignore_case=True,
            sentence=True
        )

        self.session = PromptSession(
            completer=command_completer,
            style=get_prompt_style()
        )

    def run(self):
        print("Welcome to the assistant bot!")
        self.setup_prompt()

        try:
            while True:
                try:
                    user_input = self.session.prompt("Enter command: ")
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

                result = self.handler.execute(command, args)
                if result:
                    print(result)

                if command in MODIFY_COMMANDS:
                    self.storage.save(self.book)

        finally:
            self.storage.save(self.book)


def main():
    storage_type = sys.argv[1] if len(sys.argv) > 1 else 'pickle'

    try:
        bot = AssistantBot(storage_type)
        bot.run()
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Supported storage types: {', '.join(StorageFactory.get_supported_types())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
