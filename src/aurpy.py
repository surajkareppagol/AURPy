import json
import os
import subprocess
from os import getenv, path

import requests

from console import Terminal

console = Terminal()


class AURPy:
    def __init__(self, package) -> None:
        """
        Init AURPy.
        Usage: aurpy = AURPy(package)
        Returns: None
        """

        self.package = package
        self.url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={package}"

    def search_pkg(self) -> None:
        """
        Search for a package.
        Usage: package = aurpy.search_package()
        Returns: None
        """

        response = requests.get(self.url)
        self.package_info = json.loads(response.json())
        self.package_count = self.package_info["resultcount"]

    def build(package_install: str) -> None:
        base_path = getenv("HOME")

        if not path.isdir(f"{base_path}/.aurpy"):
            os.mkdir(f"{base_path}/.aurpy")

        os.chdir(f"{base_path}/.aurpy")

        package_aur_url = f"https://aur.archlinux.org/{package_install}.git"
        subprocess.call(["git", "clone", package_aur_url])

        os.chdir(package_install)

        subprocess.call(["sudo", "makepkg", "-si"])

    def display_info(self) -> None:
        """
        Display results.
        Usage: display_info()
        Returns: None
        """

        columns = ["ID", "Package", "Description"]
        rows = self.package_info["results"]

        table = console.create_table(self.package_count, columns, rows)

        console.print(
            "[bold red]Warning[/bold red]: [bold white]This is just a experimental project, use it in virtual environment.[/bold white]"
        )

        console.print(table)

        while True:
            package_index = console.input("📦 Select One Package (1 or 2 or ...): ")

            if package_index.isdigit():
                break

        package_install = self.package_info["results"][package_index - 1]["Name"]

        self.build(package_install)

    def install(self) -> None:
        """
        Install package.
        Usage: aurpy.install()
        Returns: None
        """

        self.search_pkg()
        self.display_info()
