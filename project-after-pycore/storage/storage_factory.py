"""Factory for creating storage instances based on file type."""
from pathlib import Path
from .storage_interface import StorageInterface
from .pickle_storage import PickleStorage
from .json_storage import JSONStorage
from .csv_storage import CSVStorage


class StorageFactory:
    """Factory class for creating appropriate storage instances."""
    
    STORAGE_TYPES = {
        'pickle': PickleStorage,
        'pkl': PickleStorage,
        'json': JSONStorage,
        'csv': CSVStorage,
    }
    
    @staticmethod
    def create_storage(storage_type: str, base_path: Path = None) -> StorageInterface:
        """
        Create storage instance based on type.
        
        Args:
            storage_type: Type of storage ('pickle', 'json', 'csv')
            base_path: Base directory path (optional)
        
        Returns:
            StorageInterface instance
        
        Raises:
            ValueError: If storage type is not supported
        """
        storage_type = storage_type.lower()
        
        if storage_type not in StorageFactory.STORAGE_TYPES:
            raise ValueError(
                f"Unsupported storage type: {storage_type}. "
                f"Supported types: {', '.join(StorageFactory.STORAGE_TYPES.keys())}"
            )
        
        # Create file path
        if base_path is None:
            base_path = Path(__file__).resolve().parent.parent / "files"
        
        file_path = base_path / f"addressbook.{storage_type}"
        
        # Create and return storage instance
        storage_class = StorageFactory.STORAGE_TYPES[storage_type]
        return storage_class(file_path)
    
    @staticmethod
    def get_supported_types() -> list[str]:
        """Get list of supported storage types."""
        return list(StorageFactory.STORAGE_TYPES.keys())
