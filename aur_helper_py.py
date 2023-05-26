import requests
import os
import subprocess
import json

package_name = input("Enter the package name: ")

response = json.loads(requests.get(f"https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={package_name}").text)

if(response["resultcount"] == 0):
  print(f"Error: Couldn't able to find package \"{package_name}\"")
elif(response["results"][0]["Name"] == package_name):
  subprocess.run(["git", "clone", f"https://aur.archlinux.org/{package_name}.git"])
  os.chdir(f"{package_name}")
  subprocess.run(["makepkg", "-si"])

