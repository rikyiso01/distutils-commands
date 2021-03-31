from distutils.cmd import Command
from distutils.dist import Distribution
from typing import Callable,Type,Dict
from setuptools.sandbox import run_setup
from functools import partial
from inspect import getfullargspec
from sys import argv

commands:Dict[str,Type[Command]]={}

def get_cmdclass():
    return commands.copy()

def convert_argv(program:str):
    start=False
    for a in range(len(argv)):
        if argv[a]==program:
            start=True
        elif start:
            if argv[a].startswith('-'):
                if '=' not in argv[a]:
                    argv[a]+='=True'
            else:
                start=False

def command(name:str)->Callable[[Callable],Type[Command]]:
    return partial(generate_command,name)

def generate_command(name:str,function:Callable)->Callable:
    convert_argv(name)
    specs=getfullargspec(function)

    class Result(Command):
        description=function.__doc__
        user_options=[(arg.replace('_','-')+'=',None,None) for arg in specs.args]

        def __init__(self,*args):
            if len(args)>0 and isinstance(args[0],Distribution):
                super(Result, self).__init__(args[0])
            else:
                self.initialize_options()
                for a in range(len(args)):
                    setattr(self,specs.args[a],args[a])
                self.finalize_options()
                self.run()

        def initialize_options(self) -> None:
            defaults=len(specs.defaults) if specs.defaults is not None else 0
            for a in range(len(specs.args)):
                value=None
                if a>=len(specs.args)-defaults:
                    value=specs.defaults[a-len(specs.args)+defaults]
                setattr(self,specs.args[a],value)

        def finalize_options(self) -> None:
            for arg in specs.args:
                assert getattr(self,arg) is not None,f'Missing required option: {arg}'

        def run(self) -> None:
            function(**{arg:getattr(self,arg) for arg in specs.args})
    commands[name]=Result
    return Result

def call(name:str):
    run_setup('setup.py',[name])

def __getattr__(name:str)->Callable:
    return partial(call,name)
