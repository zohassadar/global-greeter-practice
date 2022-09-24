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

requirement_groups = ["main"]


print("Opening pyproject.toml...", end="", flush=True)
try:
    with open("pyproject.toml") as file:
        pyproject = tomlkit.load(open("pyproject.toml"))
        print("Done")
except Exception as exc:
    print("Error")
    print(f"Exception: {type(exc).__name__}")
    sys.exit(ERROR)

print("Identifying version and module...", end="", flush=True)
try:
    module = pyproject["tool"]["poetry"]["name"].replace("-", "_")
    version = pyproject["tool"]["poetry"]["version"]
    requirement_groups.extend(pyproject["tool"]["poetry"]["group"])
    print("Done")
except IndexError:
    print("Error")
    print("Unexpected pyproject.toml format")
    sys.exit(ERROR)

print(f"Loading {module}...", end="", flush=True)
try:
    loaded_module = importlib.import_module(module)
    print("Done")
except Exception as exc:
    print("Error")
    print(f"Exception: {type(exc).__name__}")
    sys.exit(ERROR)

print(f"Writing version to {module}.__init__...", end="", flush=True)
try:
    loaded_module.__file__ = typing.cast(str, loaded_module.__file__)
    open(loaded_module.__file__, "w+").write(f'__version__ = "{version}"\n')
    print("Done")
except Exception as exc:
    print("Error")
    print(f"Exception: {type(exc).__name__}")
    sys.exit(ERROR)


# for filename, command in REQUIREMENTS.items():
for group in requirement_groups:
    filename = "requirements" + ("" if group == "main" else f"-{group}") + ".txt"
    command = f"poetry export --without-hashes --only {group}"
    print(f"Opening {filename}...", end="", flush=True)
    with open(filename, "w+") as file:
        try:
            raw_output = subprocess.check_output(command.split())
            print("Done")
            print("Writing requirements...", end="", flush=True)
        except subprocess.CalledProcessError:
            print("Error")
            print(f"Unable to execute command: {command}")
            sys.exit(ERROR)
        file.write(raw_output.decode("ascii"))
        print("Done")
