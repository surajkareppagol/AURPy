import json
import os
import re
import requests
import subprocess
import sys

from rich.console import Console

console = Console()


def error_text(msg):
    return f"\n[red bold]Error[/red bold]: {msg}"


def success_text(msg):
    return f"[bright_green bold]Success[/bright_green bold]: {msg}"


class AUR:
    def __init__(self, pkg_name):
        self.pkg_name = pkg_name
        self.pkg_url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={pkg_name}"

        self.get_json()

    def get_json(self):
        response = requests.get(self.pkg_url)
        self.pkg_info = json.loads(response.text)

    def install_pkg(self, pkg_name):
        pkg_aur_url = f"https://aur.archlinux.org/{pkg_name}.git"
        subprocess.run(["git", "clone", pkg_aur_url])
        os.chdir(pkg_name)
        subprocess.run(["makepkg", "-si"])

    def search_and_install_pkg(self):
        total_pkgs = self.pkg_info["resultcount"]

        console.print(success_text(f"Found {total_pkgs} Package's."))

        if total_pkgs == 0:
            console.print(error_text(f'🚫 Package "{self.pkg_name}" Not Found.'))
            sys.exit(1)
        elif total_pkgs == 1 and self.pkg_info["results"][0]["Name"] == self.pkg_name:
            self.install_pkg(self.pkg_name)
        else:
            pkg_name_regex = re.compile(f"{self.pkg_name}")

            for index, pkg in enumerate(self.pkg_info["results"], start=1):
                pkg_content_match = pkg_name_regex.search(pkg["Name"])
                description = (
                    pkg["Description"]
                    if pkg["Description"] != None
                    else "No Description Found"
                )
                if pkg_content_match != None:
                    console.print(
                        f"{index} : [green_yellow]{pkg['Name']}[/green_yellow] - {description}",
                    )

            selected_pkg = int(input("\n📦️ Select One Package (1 or 2 or ...): "))
            selected_pkg_to_install = self.pkg_info["results"][selected_pkg - 1]["Name"]
            self.install_pkg(selected_pkg_to_install)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        console.print(error_text("Provide A Package Name."))
        sys.exit()

    try:
        aur = AUR(sys.argv[1])
        aur.search_and_install_pkg()
    except KeyboardInterrupt:
        console.print(error_text("Terminated With CTRL + C."))
