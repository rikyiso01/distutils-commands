from setuptools import setup,find_packages
from distutils_commands import command,pytest,clean,publish_pypi,wheel,source,publish_github

@command
def publish():
    pass

@command
def test_all():
    pytest('main.py')

@command
def publish(test:bool=False):
    source()
    wheel()
    publish_pypi(test)
    publish_github(test)
    clean()

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='distutils-commands',
    version='1.0',
    description='A simpler way to use distutils commands',
    license="GPL-3",
    long_description=long_description,
    author='Riccardo Isola',
    author_email='riky.isola@gmail.com',
    url="https://github.com/RikyIsola/python-matrix-tuple",
    packages=find_packages(),
    install_requires=['pytest','linux-commands','twine','wheel'],
    cmdclass={'publish':publish,'test':test_all,'clean':clean}
)
