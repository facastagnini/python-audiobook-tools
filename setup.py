#!/usr/bin/env python
# -*- coding: utf-8 -*-
# source: https://github.com/navdeep-G/setup.py/blob/master/setup.py

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# ------------------------------------------------
# Package meta-data.
NAME = "audiobook_tools"
DESCRIPTION = "A swiss army knife for audiobook metadata enrich."
URL = "https://github.com/facastagnini/python-audiobook-tools"
EMAIL = "spam@191161.xyz"
AUTHOR = "Diego Alifano, Federico Castagnini"
REQUIRES_PYTHON = ">=3.6.0"
# ------------------------------------------------


here = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
with io.open(os.path.join(here, "requirements.in"), encoding="utf-8") as f:
    required = f.read().split()

# What packages are required for this module to be tested?
with io.open(os.path.join(here, "requirements-dev.in"), encoding="utf-8") as f:
    tests_required = f.read().split()
    tests_required.pop(0)  # remove the first line, its the -r requirements.txt

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, "audiobook_tools", "__version__.py")) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={
        "console_scripts": ["audiobook_tools=audiobook_tools.__main__:main"],
    },
    install_requires=required,
    # tests_require=tests_required,
    # extras_require={
    #     'testing': tests_required
    # },
    include_package_data=True,
    license="GPL",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: GPL License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
