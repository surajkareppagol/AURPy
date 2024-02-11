import json
import os
import subprocess
from os import getenv, path
from sys import exit

import requests

from console import Terminal
from util import Util

console = Terminal()
util = Util()


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
        self.package_info = json.loads(response.text)
        self.package_count = self.package_info["resultcount"]

    def build(self, package_install: str) -> None:
        base_path = getenv("HOME")

        if not path.isdir(f"{base_path}/.aurpy"):
            os.mkdir(f"{base_path}/.aurpy")

        os.chdir(f"{base_path}/.aurpy")

        package_aur_url = f"https://aur.archlinux.org/{package_install}.git"
        subprocess.call(["git", "clone", package_aur_url])

        os.chdir(package_install)

        subprocess.call(["makepkg", "-si"])

    def display_info(self) -> None:
        """
        Display results.
        Usage: display_info()
        Returns: None
        """

        columns = ["ID", "Package", "Description"]
        rows = self.package_info["results"]

        table = console.create_table(self.package_count, columns, rows)

        def print_warning():
            console.clear()
            console.print_panel("[bold yellow]AURPy[/bold yellow] - AUR Helper")
            console.print(
                "[bold red]Warning[/bold red]: [bold white]This Is Just An Experimental Project, It Might Be Dangerous, Use It In A Virtual Environment.[/bold white]"
            )

        print_warning()

        console.print(table)

        try:
            while True:
                package_index = console.input(
                    f"📦 Select One Package (1, ..., {self.package_count}): "
                )

                if package_index.isdigit() and int(package_index) <= self.package_count:
                    break

                print_warning()

                console.print(table)
        except KeyboardInterrupt:
            console.print(util.format_text("Terminated With CTRL + C.", 0))
            exit(1)

        package_install = self.package_info["results"][int(package_index) - 1]["Name"]

        self.build(package_install)

    def install(self) -> None:
        """
        Install package.
        Usage: aurpy.install()
        Returns: None
        """

        self.search_pkg()
        self.display_info()
