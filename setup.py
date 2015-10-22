# coding: utf-8

import os
import sys
import re

from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand


def get_requirements(filename):
    requirements = []
    with open(filename) as requirements_file:
        for requirement in requirements_file:
            requirements.append(requirement.strip())


def get_version(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    version = "0.0.0"
    with open(os.path.join(here, filename)) as changes:
        for line in changes:
            version = line.strip()
            if re.search('^[0-9]+\.[0-9]+(\.[0-9]+)?$', version):
                break

    return version


class VersionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(get_version("CHANGES.rst"))


# noinspection PyAttributeOutsideInit
class PyTestCommand(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def _test_args(self):
        return []

    def initialize_options(self):
        super().initialize_options()
        self.pytest_args = []

    def finalize_options(self):
        super().finalize_options()
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="ami-push",
    version="0.1.0",
    url="https://github.com/osantana/ami-push",
    author="Osvaldo Santana Neto",
    author_email="amipush@osantana.me",
    description="Daemon that makes a bridge to listen Asterisk Management Interface (AMI) Events and send HTTP requests",
    long_description=open('README.rst').read(),
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    entry_points={
        'console_scripts': [
            "amipush = ami_push.cli:main"
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    tests_require=['pytest'],
    cmdclass={'version': VersionCommand, 'test': PyTestCommand},
)
