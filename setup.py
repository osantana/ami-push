# coding: utf-8

import os
import re

from setuptools import setup, find_packages, Command


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


setup(
    name="concord",
    version="0.1.0",
    url="https://github.com/osantana/concord",
    author="Osvaldo Santana Neto",
    author_email="concord@osantana.me",
    description="Bridge to listen Asterisk Management Interface (AMI) Events and send HTTP requests",
    long_description=open('README.rst').read(),
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    entry_points={
        'console_scripts': [
            "concord = concord.cli:main"
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={'version': VersionCommand},
    test_suite='nose.collector'
)
