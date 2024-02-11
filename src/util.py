class Util:
    def __init__(self) -> None:
        """
        Init util.
        Usage: util = Util()
        Returns: None
        """

        pass

    def format_text(self, string: str, status: int) -> str:
        """
        Format text.
        Usage: format_text(string, status)
        Returns: str
        """

        if status:
            return f"[red bold]Error[/red bold]: {string}"
        else:
            return f"[green bold]Success[/green bold]: {string}"
