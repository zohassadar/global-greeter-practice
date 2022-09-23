#!/usr/bin/env python
# Run this crap to work around tox and poetry not getting along natively
# This also adds __version__ to __init__
from __future__ import annotations

import importlib
import subprocess
import sys
import typing

import tomlkit

ERROR = 1
REQUIREMENTS = {
    "requirements-dev.txt": "poetry export --without-hashes --only dev",
    "requirements.txt": "poetry export --without-hashes",
}

for filename, command in REQUIREMENTS.items():
    print(f"Opening {filename}...", end="")
    with open(filename, "w+") as potato:
        try:
            raw_output = subprocess.check_output(command.split())
            print("Done")
            print(f"Writing requirements...", end="")
        except subprocess.CalledProcessError:
            print("Error")
            print(f"Unable to execute command: {command}")
            sys.exit(ERROR)
        potato.write(raw_output.decode("ascii"))
        print("Done")


print(f"Opening pyproject.toml...", end="")
try:
    with open("pyproject.toml") as file:
        pyproject = tomlkit.load(open("pyproject.toml"))
        print("Done")
except Exception as exc:
    print("Error")
    print(f"Exception: {type(exc).__name__}")
    sys.exit(ERROR)

print("Identifying version and module...", end="")
try:
    module = pyproject["tool"]["poetry"]["name"].replace("-", "_")
    version = pyproject["tool"]["poetry"]["version"]
    print("Done")
except IndexError:
    print("Error")
    print("Unexpected pyproject.toml format")
    sys.exit(ERROR)

print(f"Loading {module}...", end="")
try:
    loaded_module = importlib.import_module(module)
    print("Done")
except Exception as exc:
    print("Error")
    print(f"Exception: {type(exc).__name__}")
    sys.exit(ERROR)

print(f"Writing version to {module}.__init__...", end="")
try:
    typing.cast(str, loaded_module.__file__)
    open(loaded_module.__file__, "w+").write(f'__version__ = "{version}"\n')
    print("Done")
except Exception as exc:
    print("Error")
    print(f"Exception: {type(exc).__name__}")
    sys.exit(ERROR)
