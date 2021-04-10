from distutils_commands import command,wheel,publish_github,publish_pypi,source,clean,pdoc,pytest,get_cmdclass,\
    local_install
from shutil import rmtree
from pytest import raises
from random import randint
from os import rename,listdir
from sys import executable
from subprocess import run,PIPE

def test_clean():
    clean()
    clean()

def test_pdoc():
    pdoc('distutils_commands.commands')
    rmtree('docs')

def test_pytest():
    pytest('tests/innertest.py')

def test_wheel():
    wheel()
    clean()

def test_source():
    source()
    clean()

def test_publish_github():
    wheel()
    version=str(randint(0,100))
    spoof_version(version)
    publish_github('Testing',True,version)
    clean()

def test_publish_pypi():
    wheel()
    version=str(randint(0,100))
    spoof_version(version)
    publish_pypi(True,version)
    clean()

def test_local_install():
    local_install()
    assert 'distutils-commands' in run([executable,'-m','pip','freeze'],stdout=PIPE,check=True,text=True).stdout
    run([executable,'-m','pip','uninstall','-y','distutils-commands'],check=True)


def test_get_cmdclass():
    assert len(get_cmdclass())>0

def test_command():
    @command('cmd')
    def cmd():
        raise AssertionError()
    with raises(AssertionError):
        cmd()

def spoof_version(version:str):
    file=['dist/'+file for file in listdir('dist') if file.endswith('.whl')][0]
    rename(file,f'dist/distutils_commands-{version}-py3-none-any.whl')
