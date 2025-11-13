"""Storage interface for different file formats."""
from abc import ABC, abstractmethod
from pathlib import Path


class StorageInterface(ABC):
    """Abstract base class for storage implementations."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure the directory for the file exists."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def save(self, data: object) -> bool:
        """Save data to file."""
        pass
    
    @abstractmethod
    def load(self) -> object:
        """Load data from file."""
        pass
