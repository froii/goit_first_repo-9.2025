"""CSV storage implementation."""
import csv
from pathlib import Path
from .storage_interface import StorageInterface
from .decorators import handle_save_errors, handle_load_errors


class CSVStorage(StorageInterface):
    """Storage implementation using CSV format."""
    
    @handle_save_errors
    def save(self, data: object) -> bool:
        """Save data to CSV file."""
        rows = self._serialize(data)
        
        if not rows:
            return True
        
        with open(self.file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True
    
    @handle_load_errors
    def load(self) -> list:
        """Load data from CSV file."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def _serialize(self, obj) -> list[dict]:
        """Convert object to list of flat dicts for CSV."""
        rows = []
        
        # Handle AddressBook
        if hasattr(obj, 'data') and isinstance(obj.data, dict):
            for name, record in obj.data.items():
                phones = "; ".join(p.value for p in record.phones) if hasattr(record, 'phones') else ""
                birthday = record.birthday.value.strftime("%d.%m.%Y") if hasattr(record, 'birthday') and record.birthday else ""
                
                rows.append({
                    "name": name,
                    "phones": phones,
                    "birthday": birthday
                })
        
        return rows
