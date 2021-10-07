import os
import re

from setuptools import setup, find_packages

with open("requirements.txt") as rf:
    requirements = rf.readlines()

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog:", "")


def find_version(*file_paths):
    """
    This pattern was modeled on a method from the Python Packaging User Guide:
        https://packaging.python.org/en/latest/single_source_version.html
    We read instead of importing so we don't get import errors if our code
    imports from dependencies listed in install_requires.
    """
    base_module_file = os.path.join(*file_paths)
    with open(base_module_file) as f:
        base_module_data = f.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", base_module_data, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="mdssdk",
    version=find_version("mdssdk", "__init__.py"),
    description="Python SDK for Cisco MDS Switches",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Cisco Systems, Inc.",
    author_email="subharad@cisco.com",
    packages=find_packages(exclude=("test",)),
    url="https://github.com/Cisco-SAN/mdslib",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
