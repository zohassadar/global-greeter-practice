import tomlkit
import re
import importlib


pyproject = tomlkit.load(open("pyproject.toml"))
version = pyproject["tool"]["poetry"]["version"]


for package in pyproject["tool"]["poetry"]["packages"]:
    include = package["include"]
    module = importlib.import_module(include)
    loaded = open(module.__file__).read()
    replaced = re.sub(
        r'^__version__\ *=\ *"([^"]*)"',
        f'__version__ = "{version}"',
        loaded,
        flags=re.M,
    )
    open(module.__file__, "w+").write(replaced)
