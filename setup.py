from setuptools import setup,find_packages
from distutils_commands import command,clean,publish_pypi,wheel,source,publish_github,get_cmdclass,pytest

@command('publish')
def publish(changelog:str):
    test()
    clean()
    source()
    wheel()
    publish_github(changelog)
    publish_pypi()
    clean()

@command('test')
def test():
    pytest('tests/tests.py')

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='distutils-commands',
    version='1.5.4',
    description='A simpler way to use distutils commands',
    license="GPL-3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Riccardo Isola',
    author_email='riky.isola@gmail.com',
    url="https://github.com/RikyIsola/distutils-commands",
    packages=find_packages(),
    setup_requires=['twine>=3.4.1','wheel>=0.36.2','pytest>=6.2.2'],
    extras_require={'pytest':'pytest>=6.2.2','pypi':'twine>=3.4.1','wheel':'wheel>=0.36.2','pdoc':'pdoc>=6.4.2'},
    cmdclass=get_cmdclass(),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9'],
    keywords='distutils setuptools commands',
    python_requires='>=3.7',
    project_urls={'Tracker':'https://github.com/RikyIsola/distutils-commands/issues'}
)
