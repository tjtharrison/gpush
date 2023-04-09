"""
Setup file for python-semantic-versioning
"""
from setuptools import setup

with open("README.md", encoding="UTF-8") as readme_file:
    readme_contents = readme_file.read()

__version__ = "1.1.1"

setup(
    name="gpush",
    version=__version__,
    long_description=readme_contents,
    long_description_content_type="text/markdown",
)
