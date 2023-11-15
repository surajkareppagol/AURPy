import json
import os
import re
import requests
import subprocess
import sys

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


# Util Functions
def error_text(msg: str) -> str:
    return f"\n[red bold]Error[/red bold]: {msg}"


def success_text(msg: str) -> str:
    return f"[bright_green bold]Success[/bright_green bold]: {msg}"


def search_pkg(url: str) -> dict | int:
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        console.print(error_text("🚫 Something Went Wrong."))
        sys.exit(1)

    pkg_info = json.loads(response.text)

    if response.status_code == 200:
        return pkg_info
    return 0


def create_table(packages: int) -> Table:
    table = Table(title=f"📦 Found {packages} Packages", title_style="bold")
    table.add_column("ID", justify="left")
    table.add_column("Name", justify="left")
    table.add_column("Description", justify="left")
    return table

def create_pkg_name(start:int, end:int, pkg_name: str) -> str:
    return f"[white]{pkg_name[:start]}[/white][green_yellow]{pkg_name[start:end + 1]}[/green_yellow][white]{pkg_name[end + 1:]}[/white]"

# Set Console
console = Console()
console.print(Panel("Arch AUR Py"))


# Install Package
def build_and_install(pkg_name: str) -> None:
    try:
        os.mkdir(f"{os.getenv("HOME")}/.aurpy")
    except FileExistsError:
        pass

    os.chdir(f"{os.getenv("HOME")}/.aurpy")
    pkg_aur_url = f"https://aur.archlinux.org/{pkg_name}.git"
    subprocess.call(["git", "clone", pkg_aur_url])
    os.chdir(pkg_name)
    subprocess.call(["makepkg", "-si"])


def install_pkg(pkg_info: dict) -> None:
    total_pkgs = pkg_info["resultcount"]
    pad = len(str(total_pkgs))

    if not total_pkgs:
        console.print(error_text(f'🚫 Package "{pkg_name}" Not Found.'))
        sys.exit(1)

    table = create_table(total_pkgs)

    pkg_name_regex = re.compile(f"{pkg_name}")

    for index, pkg in enumerate(pkg_info["results"], start=1):
        pkg_content_match = pkg_name_regex.search(pkg["Name"])

        description = (
            pkg["Description"]
            if pkg["Description"] is not None
            else "No Description Found"
        )

        if pkg_content_match is not None:
            table.add_row(
                f"{index}".zfill(pad),
                create_pkg_name(pkg_content_match.start(), pkg_content_match.end(), pkg["Name"]),
                f"{description}",
            )

    console.print(table)

    selected_pkg = int(console.input("\n📦 Select One Package (1 or 2 or ...): "))

    selected_pkg_to_install = pkg_info["results"][selected_pkg - 1]["Name"]

    build_and_install(selected_pkg_to_install)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            console.print(error_text("Provide A Package Name."))
            sys.exit()

        pkg_name = sys.argv[1]
        pkg_url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={pkg_name}"

        pkg_json = search_pkg(pkg_url)

        if not pkg_json:
            console.print(error_text("🚫 Something Went Wrong."))
            sys.exit(1)

        install_pkg(pkg_json)
    except KeyboardInterrupt:
        console.print(error_text("Terminated With CTRL + C."))
