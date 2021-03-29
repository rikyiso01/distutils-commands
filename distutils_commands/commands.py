from .distutils_command import bdist_wheel,sdist,command
from os import listdir
from os.path import exists,join
from shutil import rmtree
from sys import argv
from pathlib import Path

@command
def clean():
    if exists('.pytest_cache'):
        rmtree('.pytest_cache')
    if exists('build'):
        rmtree('build')
    if exists('dist'):
        rmtree('dist')
    for file in [file for file in listdir('.') if file.endswith('.egg-info')]:
        rmtree(file)
    if exists('temp'):
        rmtree('temp')

@command
def pdoc():
    try:
        from pdoc.render import configure
        from pdoc import pdoc
    except ImportError:
        raise import_exception('pdoc')
    configure(docformat='google')
    pdoc('matrix',output_directory=Path('docs'))

@command
def pytest(file:str):
    try:
        from pytest import main as pytest_main
    except ImportError:
        raise import_exception('pytest')
    pytest_main([file])

@command
def wheel():
    try:
        import wheel
    except ImportError:
        raise import_exception('wheel')
    bdist_wheel()

@command
def source():
    sdist()

def get_version()->str:
    version:str=[line for line in open('setup.py').readlines() if 'version' in line][-1].strip().replace(' ','')
    version=version[version.find('version=')+9:]
    version=version[:version.find(',')-1]
    return version

@command
def publish_github(test:bool=False):
    try:
        from linux_commands import gh,git
    except ImportError:
        raise import_exception('github')
    version=get_version()
    changelog:str=input('Write the changelog: ')
    git.add('.')
    try:
        git.commit(m=changelog)
        git.push()
    except OSError:
        pass
    try:
        gh.release.create(version,prerelease=version<'1.0',notes=changelog,title=f'v{version}',
                          *[join('dist',file) for file in listdir('dist')])
    except OSError:
        raise FileExistsError('This version is already published on github')
    if test:
        gh.release.delete(version)
        git.push('origin',version,delete=True)

@command
def publish_pypi(test:bool=False):
    try:
        from twine.__main__ import main as twine
    except ImportError:
        raise import_exception('pypi')
    backup=argv.copy()
    argv.clear()
    argv.append(backup[0])
    argv.append('upload')
    if test:
        argv.append('--repository')
        argv.append('testpypi')
    version=get_version()
    argv.extend([join('dist',file) for file in listdir('dist') if version in file])
    result=twine()
    if result is not None:
        raise FileExistsError('This version is already published on Pypi')
    argv.clear()
    argv.extend(backup)

def import_exception(name:str)->ImportError:
    return ImportError(f'{name} extension dependencies not installed')
