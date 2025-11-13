"""File storage for address book data."""
import pickle
from pathlib import Path
from models import AddressBook


class FileStorage:
    """Handles saving and loading address book data."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def save(self, book: AddressBook) -> bool:
        """Save address book to file."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "wb") as f:
                pickle.dump(book, f)
            return True
        except (IOError, OSError) as e:
            print(f"Can't save data in file {self.file_path}: {e}")
            return False

    def load(self) -> AddressBook:
        """Load address book from file."""
        try:
            with open(self.file_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"File {self.file_path} not found, a new book has been created")
            return AddressBook()
        except (pickle.UnpicklingError, EOFError, AttributeError):
            print(f"File {self.file_path} is corrupted, a new book has been created")
            return AddressBook()
        except Exception as e:
            print(f"Can't load data from file {self.file_path}: {e}")
            return AddressBook()
