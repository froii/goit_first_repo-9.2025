"""Table rendering utilities using Rich."""
from rich.console import Console
from rich.table import Table


class TableRenderer:
    """Handles rendering tables for displaying data."""
    
    def __init__(self):
        self.console = Console()

    def render(self, title: str, columns: list[dict], rows: list[list], markup: bool = False):
        """Render a table with the given title, columns, and rows."""
        table = Table(title=title, show_header=True, header_style="bold cyan")

        for col in columns:
            table.add_column(
                col.get("name", ""),
                style=col.get("style", "white"),
                width=col.get("width", None)
            )

        for row in rows:
            table.add_row(*row)

        self.console.print(table, markup=markup)
