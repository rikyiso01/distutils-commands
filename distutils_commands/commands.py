from .distutils_command import bdist_wheel,sdist,command
from os import listdir
from os.path import exists,join
from shutil import rmtree
from pytest import main as pytest_main
from twine.__main__ import main as twine
from sys import argv
from linux_commands import gh,git

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
def pytest(file:str):
    pytest_main([file])

@command
def wheel():
    bdist_wheel()

@command
def source():
    sdist()

@command
def publish_github(test:bool=False):
    version:str=[line for line in open('setup.py').readlines() if 'version' in line][-1].strip().replace(' ','')
    version=version[version.find('version=')+9:]
    version=version[:version.find(',')-1]
    print(version)
    changelog:str=input('Write the changelog:')
    git.add('.')
    try:
        git.commit(m=changelog)
        git.push()
    except OSError:
        pass
    gh.release.create(version,prerelease=version<'1.0',notes=changelog,title=f'V{version}',
                      *[join('dist',file) for file in listdir('dist')])
    if test:
        gh.release.delete(version)
        git.push('origin',version,delete=True)

@command
def publish_pypi(test:bool=False):
    backup=argv.copy()
    argv.clear()
    argv.append(backup[0])
    argv.append('upload')
    if test:
        argv.append('--repository')
        argv.append('testpypi')
    argv.extend([join('dist',file) for file in listdir('dist')])
    twine()
    argv.clear()
    argv.extend(backup)
