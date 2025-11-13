"""Pickle storage implementation."""
import pickle
from pathlib import Path
from .storage_interface import StorageInterface
from .decorators import handle_save_errors, handle_load_errors


class PickleStorage(StorageInterface):
    """Storage implementation using pickle format."""
    
    @handle_save_errors
    def save(self, data: object) -> bool:
        """Save data to pickle file."""
        with open(self.file_path, "wb") as f:
            pickle.dump(data, f)
        return True
    
    @handle_load_errors
    def load(self) -> object:
        """Load data from pickle file."""
        with open(self.file_path, "rb") as f:
            return pickle.load(f)
