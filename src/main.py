#!/usr/bin/python3

from sys import argv, exit

from aurpy import AURPy
from console import Terminal
from util import Util

console = Terminal()
util = Util()

if __name__ == "__main__":
    try:
        if len(argv) == 1:
            console.print(util.format_text("Provide A Package Name.", 0))
            exit(1)

        package = argv[1]

        aurpy = AURPy(package)

        aurpy.install()
    except KeyboardInterrupt:
        console.print(util.format_text("Terminated With CTRL + C."))
