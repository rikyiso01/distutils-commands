from distutils.cmd import Command
from distutils.dist import Distribution
from typing import Callable,Type
from setuptools.sandbox import run_setup
from functools import partial
from inspect import getfullargspec

def command(function:Callable)->Type[Command]:
    specs=getfullargspec(function)

    class Result(Command):
        user_options=[(arg.replace('_','-'),None,None) for arg in specs.args]

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
            for a in range(defaults):
                setattr(self,specs.args[-(defaults+a)],specs.defaults[a-defaults])

        def finalize_options(self) -> None:
            for arg in specs.args:
                assert hasattr(self,arg),f'Missing required option: {arg}'

        def run(self) -> None:
            function(**{arg:getattr(self,arg) for arg in specs.args})
    return Result

def call(name:str):
    run_setup('setup.py',[name])

def __getattr__(name:str)->Callable:
    return partial(call,name)
