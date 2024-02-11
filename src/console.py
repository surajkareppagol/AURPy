from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Terminal(Console):
    def __init__(self) -> None:
        """
        Init Terminal.
        Usage: console = Terminal()
        Returns: None
        """
        super().__init__()

        self.table = Table()

    def add_columns(self, columns: list) -> None:
        """
        Add columns.
        Usage: add_columns(columns)
        Returns: None
        """

        for column in columns:
            self.table.add_column(column, justify="left")

    def add_rows(self, rows: list) -> None:
        """
        Add rows.
        Usage: add_rows(rows)
        Returns: None
        """

        for index, package in enumerate(rows, start=1):
            description = (
                "No Description Found"
                if package["Description"] is None
                else package["Description"]
            )

            self.table.add_row(str(index), package["Name"], description)

    def create_table(self, packages: int, columns: list, rows: list) -> Table:
        """
        Create table.
        Usage: console.create_table(packages, columns, rows)
        Returns: Table
        """

        self.add_columns(columns)
        self.add_rows(rows)

        return self.table

    def print_panel(self, string: str) -> None:
        """
        Print message in panel.
        Usage: console.print_panel(string)
        Returns: None
        """

        super().print(Panel(string))
