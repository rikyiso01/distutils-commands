from setuptools import setup,find_packages
from distutils_commands import command,clean,publish_pypi,wheel,source,publish_github,get_cmdclass

@command('publish')
def publish(changelog:str,test:bool=False):
    source()
    wheel()
    publish_github(changelog,test)
    publish_pypi(test)
    clean()

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='distutils-commands',
    version='1.4.2',
    description='A simpler way to use distutils commands',
    license="GPL-3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Riccardo Isola',
    author_email='riky.isola@gmail.com',
    url="https://github.com/RikyIsola/distutils-commands",
    packages=find_packages(),
    setup_requires=['linux-commands','twine','wheel'],
    extras_require={'pytest':'pytest','github':'linux-commands','pypi':'twine','wheel':'wheel','pdoc':'pdoc'},
    cmdclass=get_cmdclass(),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3.9'],
    keywords='distutils setuptools commands',
    python_requires='>=3.9',
    project_urls={'Tracker':'https://github.com/RikyIsola/distutils-commands/issues'}
)
