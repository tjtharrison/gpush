"""
Setup file for python-semantic-versioning
"""
from setuptools import setup

with open("README.md", encoding="UTF-8") as readme_file:
    readme_contents = readme_file.read()

with open("requirements.txt", encoding="UTF-8") as requirements_file:
    required = requirements_file.read().splitlines()

__version__ = "2.1.0"

setup(
    name="gpush",
    version=__version__,
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    install_requires=required,
    scripts=["gpush"],
)
