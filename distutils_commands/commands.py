from .distutils_commands import bdist_wheel,sdist,command
from os import listdir,environ,getcwd
from os.path import exists,join
from shutil import rmtree
from sys import argv,executable
from pathlib import Path
from subprocess import run,CalledProcessError

@command('local_install')
def local_install():
    """Locally install the package"""
    clean()
    wheel()
    if 'PYTHONPATH' in environ:
        environ['PYTHONPATH']=environ['PYTHONPATH'].replace(getcwd(),'').replace('::',':').strip(':')
    file=listdir('dist')[0]
    name=file[0:file.index('-')].replace('_','-')
    run([executable,'-m','pip','uninstall','-y',name],check=True)
    run([executable,'-m','pip','install',join('dist',file)],check=True)
    clean()

@command('clean')
def clean():
    """clean the working dir"""
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

@command('pdoc')
def pdoc(module:str,docformat:str='google',output_dir:str='docs'):
    """generate a pdoc documentation"""
    try:
        from pdoc.render import configure
        from pdoc import pdoc,Literal
    except ImportError:
        raise import_exception('pdoc')
    docformat:Literal['google']
    configure(docformat=docformat)
    pdoc(module,output_directory=Path(output_dir))

@command('pytest')
def pytest(file:str):
    """run tests with pytest"""
    try:
        from pytest import main as pytest_main,ExitCode
    except ImportError:
        raise import_exception('pytest')
    if pytest_main([file])!=ExitCode.OK:
        raise Exception('Test failed')

@command('wheel')
def wheel():
    """build the wheel"""
    try:
        import wheel
    except ImportError:
        raise import_exception('wheel')
    bdist_wheel()

@command('source')
def source():
    """create the tar.gz"""
    sdist()

def get_version()->str:
    version:str=[line for line in open('setup.py').readlines() if 'version' in line][-1].strip().replace(' ','')
    version=version[version.find('version=')+9:]
    version=version[:version.find(',')-1]
    return version

@command('publish-github')
def publish_github(changelog:str,test:bool=False,version:str=''):
    """publish the release on Github"""
    if version=='':
        version=get_version()
    if not test:
        run(['git','add','.'],check=True)
        try:
            run(['git','commit','-m',changelog],check=True)
            run(['git','push'],check=True)
        except CalledProcessError:
            pass
    print(*[join('dist',file) for file in listdir('dist') if version in file])
    process=run(['gh','release','create',version,*(['--prerelease'] if version<'1.0' else []),'--notes',changelog,
                 '--title',f'v{version}',*[join('dist',file) for file in listdir('dist') if version in file]])
    if process.returncode!=0:
        raise FileExistsError('This version is already published on github')
    if test:
        run(['gh','release','delete',version],check=True)
        run(['git','push','--delete','origin',version],check=True)

@command('publish-pypi')
def publish_pypi(test:bool=False,version:str=''):
    """publish the release on Pypi"""
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
    if version=='':
        version=get_version()
    argv.extend([join('dist',file) for file in listdir('dist') if version in file])
    result=twine()
    if result is not None:
        print(result)
        raise FileExistsError('This version is already published on Pypi')
    argv.clear()
    argv.extend(backup)

def import_exception(name:str)->ImportError:
    return ImportError(f'{name} extension dependencies not installed, '
                       f'you can install it with "pip install distutils-commands[{name}]"')
