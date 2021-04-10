# distutils-commands
A simpler way to use distutils commands

## Installation

You can install it from [Pypi](https://pypi.org/project/distutils-commands) or from the
[release section](https://github.com/RikyIsola/distutils-commands/releases)

## Usage

In your setup.py:
```python
from distutils_commands import command
@command('my-command')
def my_command():
    pass
```
this will create a distutils command that can be use in the cmdclass section

All commands are invokable from other commands:
```python
from distutils_commands import command
@command('my-command')
def my_command():
    pass
@command('my-other-command')
def my_other_command():
    my_command()
```

You can also invoke default commands from your command:
```python
from distutils_commands import bdist_wheel,command
@command('my-other-other-command')
def my_other_other_command():
    bdist_wheel()
```

You can comment a command with dosctrings
```python
from distutils_commands import bdist_wheel,command
@command('my-other-other-command')
def my_other_other_command():
    """does something"""
    bdist_wheel()
```

You can then pass the generated command to the cmdclass argument of the setup
```python
from distutils_commands import get_cmdclass
from setuptools import setup
setup(cmdclass=get_cmdclass())
```

There are already some ready-made commands to use:
```python
from distutils_commands import clean,pytest,wheel,source,publish_github,publish_pypi,pdoc
```
- clean: removes all setuptools building files like eggs and temporary folders
- pytest(name:str): run pytest with the given argument as a starting point
- wheel: at the moment identical to bdist_wheel
- source: at the moment identical to sdist
- publish_github: use the github command line program that you need to have installed, to create a release
- publish_pypi: use twine to upload the project to pypi
- pdoc: use pdoc to generate the documentation
- local_install: locally install the package using pip and wheel
