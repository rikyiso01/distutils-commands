from setuptools import setup,find_packages
from distutils_commands import command,clean,publish_pypi,wheel,source,publish_github

@command
def publish(test:bool=False):
    source()
    wheel()
    publish_github(test)
    publish_pypi(test)
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
    url="https://github.com/RikyIsola/distutils-commands",
    packages=find_packages(),
    install_requires=['pytest','linux-commands','twine','wheel'],
    cmdclass={'publish':publish,'clean':clean},
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3.9'],
    keywords='distutils setuptools commands',
    python_requires='>=3.9',
    project_urls={'Tracker':'https://github.com/RikyIsola/distutils-commands/issues'}
)
