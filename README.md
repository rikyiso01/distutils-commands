# distutils-commands
A simpler way to use distutils commands

## Installation

You can install it from [Pypi](https://pypi.org/project/distutils-commands/1.1/) or from the
[release section](https://github.com/RikyIsola/distutils-commands/releases)

## Usage

In your setup.py:
```python3
from distutils_commands import command
@command
def my_command():
  pass
```
this will create a distutils command that can be use in the cmdclass section

All commands are invokable from other commands:
```python3
@command
def my_other_command():
  my_command()
```

You can also invoke default commands from your command:
```python3
from distutils_command import bdist_wheel
@command
def my_other_other_command():
  bdist_wheel()
```

There are already some ready-made commands to use:
```python3
from distutils_command import clean,pytest,wheel,source,publish_github,publish_pypi
```
- clean: removes all setuptools building files like eggs and temporary folders
- pytest(name:str): run pytest with the given argument as a starting point
- wheel: at the moment identical to bdist_wheel
- source: at the moment identical to sdist
- publish_github: use the github command line program that you need to have installed, to create a release
- publish_pypi: use twine to upload the project to pypi
