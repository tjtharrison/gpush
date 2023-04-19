"""
Setup file for python-semantic-versioning
"""
from setuptools import setup

from _version import __version__

with open("README.md", encoding="UTF-8") as readme_file:
    readme_contents = readme_file.read()

with open("requirements.txt", encoding="UTF-8") as requirements_file:
    required = requirements_file.read().splitlines()


# Duplicate gpush.py to gpush
with open("gpush.py", "r", encoding="UTF-8") as gpush_file:
    gpush_contents = gpush_file.read()

with open("gpush", "w", encoding="UTF-8") as gpush_file:
    gpush_file.write(gpush_contents)


setup(
    name="gpush",
    version=__version__,
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    install_requires=required,
    scripts=["gpush", "_version.py"],
)
