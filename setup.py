# -*- coding: utf-8 -*-
"""Setup for OS-ENV.

Todo:
    * Test

Note:
    The _program variable is set in __init__.py.
    it determines the name of the package/final command line tool.

"""
import os
import sys
import shutil
import time
from lib import __version__, _program, _description, _author, _url
from setuptools.command.install import install
#from setuptools.command.develop import develop
#from setuptools.command.egg_info import egg_info
from setuptools import find_packages, setup


class SetupSupport:
    """This class support the setup process.

    All methods are static to made it simple.
    - SetupSupport.get_requirements("requirements.txt)
    - SetupSupport.get_long_description("README.md)

    """

    @staticmethod
    def get_requirements(filename):
        """Return content from config file.

        Args:
            filename (str): Filename for readout the requirements.
        Returns:
            list: Return a list of requirements.

        """
        with open(filename) as file_handle:
            required = [
                x for x in file_handle.read().splitlines() if not x.startswith("#")
            ]
            return required

    @staticmethod
    def get_long_description(filename):
        """Return content from markdown files."""
        with open(filename, "r") as file_handle:
            long_description = file_handle.read()
            return long_description

    @staticmethod
    def add_to_bashrc():        
        home = os.path.expanduser("~")
        bashrc = "{home_path}/.bashrc".format(home_path=home)

        # check bashrc exists
        if not os.path.isfile(bashrc):
            print("{0} file not found.".format(bashrc))
            return

        # mkdir ~/.bashrc.d
        if not os.path.isdir("{home_path}/.bashrc.d".format(home_path=home)):
            os.mkdir("{home_path}/.bashrc.d".format(home_path=home), 0o700)

        with open(bashrc, "w") as filehandler:
            if not "for file in ~/.bashrc.d/*.bashrc;" in filehandler.read():
                
                print("bashrc.d will be installed...")
                script = """
# Added by osenv
for file in ~/.bashrc.d/*.bashrc;
do
    source "$file"
done
"""
                # backup the file
                timestr = time.strftime("%Y%m%d-%H%M%S")
                shutil.copy2(src=bashrc, dst="{0}.bak.{1}".format(bashrc, timestr))

                # add new one
                filehandler.write(script)

        #if not os.path.isfile("{0}/.bashrc.d/10-osenv.bashrc".format(home)):
        shutil.copy2(src=".bashrc.d/10-osenv.bashrc", dst="{0}/.bashrc.d/10-osenv.bashrc".format(home))
        print("osenv to bashrc.d successful added.")

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print("Run post install process...")
        install.run(self)        
        SetupSupport.add_to_bashrc()


setup(
    name=_program,
    version=__version__,
    scripts=["{prog}".format(prog=_program)],
    author=_author,
    author_email="{0}@empty".format(_author),
    description=_description,
    long_description=SetupSupport.get_long_description(filename="README.md"),
    long_description_content_type="text/markdown",
    url=_url,
    packages=find_packages(),
    install_requires=SetupSupport.get_requirements(filename="requirements.txt"),
    cmdclass={'install': CustomInstallCommand},
    test_suite="tests",
    extras_require={
        "dev": SetupSupport.get_requirements(filename="requirements-dev.txt")
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        #"Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Environment :: OpenStack",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.0",
)
