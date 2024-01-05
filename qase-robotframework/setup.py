# -*- coding: utf-8 -*-
"""
    Setup file for qaseio.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup, find_packages

NAME = "qase-robotframework"
VERSION = "2.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
  "qase-python-commons>=1.0.2",
  "python-dateutil",
]

setup(
    name=NAME,
    version=VERSION,
    description="Qase Robot Framework Listener",
    author="Qase Team",
    author_email="support@qase.io",
    url="https://github.com/qase-tms/qase-python/tree/master/qase-robotframework",
    keywords=["Qase Listener", "Qase TestOps API"],
    python_requires=">=3.7",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache 2.0",
    long_description="""\
    Qase Robot Framework Listener.  # noqa: E501
    """
)
