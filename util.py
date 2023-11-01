import json
import requests
import subprocess
import os
import sys
import re


class AUR_PKG:
    def __init__(self, pkg_name):
        self.pkg_name = pkg_name

    def make_request(self):
        return requests.get(
            f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={self.pkg_name}"
        )

    def get_json(self, response):
        self.pkg_json = json.loads(response.text)

    def install_pkg(self, pkg_name):
        subprocess.run(["git", "clone", f"https://aur.archlinux.org/{pkg_name}.git"])
        os.chdir(pkg_name)
        subprocess.run(["makepkg", "-si"])

    def check_and_install_pkg(self):
        # Get JSON
        response = self.make_request()
        self.get_json(response)

        # Check For Package
        if self.pkg_json["resultcount"] == 0:
            print(f'🚫 Package "{self.pkg_name}" Not Found.')
            sys.exit(1)

        elif self.pkg_json["resultcount"] == 1:
            if self.pkg_json["results"][0]["Name"] == self.pkg_name:
                self.install_pkg(self.pkg_name)
        else:
            pkg_name_regex = re.compile(f"{self.pkg_name}")

            # Print All The Available Packages
            for index, pkg in enumerate(self.pkg_json["results"], start=1):
                if pkg_name_regex.search(pkg["Name"]) != None:
                    print(f"{index} : {pkg['Name']} - {pkg['Description']}")

            # Select A Package To Download
            selected_pkg = int(
                input("\n📦️ Found Multiple Packages, Please Select (1, 2, ..): ")
            )
            self.install_pkg(self.pkg_json["results"][selected_pkg - 1]["Name"])
