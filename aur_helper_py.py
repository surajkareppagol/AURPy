import json
import os
import re
import requests
import subprocess
import sys

pkg_name = input("📦️ Package: ")

pkg_response = requests.get(
    f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={pkg_name}"
)

pkg_json = json.loads(pkg_response.text)

# Install Package


def install_pkg(pkg_name):
    subprocess.run(["git", "clone", f"https://aur.archlinux.org/{pkg_name}.git"])
    os.chdir(pkg_name)
    subprocess.run(["makepkg", "-si"])


# If No Packages Found Exit

if pkg_json["resultcount"] == 0:
    print(f'🚫 Package "{pkg_name}" Not Found.')
    sys.exit(1)
elif pkg_json["resultcount"] == 1:
    if pkg_json["results"][0]["Name"] == pkg_name:
        install_pkg(pkg_name)
else:
    pkg_name_regex = re.compile(f"{pkg_name}")

    # Print All The Available Packages

    for index, pkg in enumerate(pkg_json["results"], start=1):
        if pkg_name_regex.search(pkg["Name"]) != None:
            print(f"{index} : {pkg['Name']} - {pkg['Description']}")

    # Select A Package To Download

    selected_pkg = int(
        input("\n📦️ Found Multiple Packages, Please Select (1, 2, ..): ")
    )
    install_pkg(pkg_json["results"][selected_pkg - 1]["Name"])
