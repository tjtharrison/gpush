"""
Test the version of the package
"""
import gpush


def test_get_version():
    """
    Function to test the get_version function in gpush.py
    :return:
    """
    with open("_version.py", "r", encoding="UTF-8") as version_file:
        current_version_contents = version_file.read()
        for line in current_version_contents.splitlines():
            if line.startswith("__version__"):
                current_version = line.split("=")[1].strip().strip('"')
                break

    assert gpush.get_version() == current_version
