"""
Tests complete functionality of gpush.py
"""

import subprocess

import pytest

from tests.bin import github


@pytest.fixture(autouse=True)
def my_fixture():
    """
    Wrapper for config unit tests to back up and restore configuration to test field manipulation.
    :return:
    """
    github.create_repo()
    github.create_readme()
    github.clone_repo()
    yield
    github.delete_repo()
    github.cleanup_local()


def test_git_commit_and_push():
    """
    Function to test the git_commit function in gpush.py with no-push.
    :return:
    """
    try:
        commands = [
            "cd gpush-test",
            "git checkout -b test-branch",
        ]
        ret = subprocess.run(
            ";".join(commands), capture_output=True, shell=True, check=True
        )
        print(ret.stdout)
        print("Branch setup locally")
    except Exception as error_message:
        print("Some error occurred while setting up the branch locally")
        print(str(error_message))
        raise

    try:
        commands = [
            "cd gpush-test",
            "touch test",
            "git add test",
            "../gpush.py --message 'fix: test commit'",
        ]
        ret = subprocess.run(
            ";".join(commands), capture_output=True, shell=True, check=True
        )
        print(ret.stdout)
        print("Commit made successfully")
        last_commit = subprocess.run(
            "cd gpush-test; git log --pretty=oneline | head -n1",
            capture_output=True,
            shell=True,
            check=True,
        )
        last_commit_message = str(last_commit.stdout)
    except Exception as error_message:
        print("Some error occurred while committing to the branch locally")
        print(str(error_message))
        raise

    if last_commit_message.endswith(" fix: test commit\\n'"):
        assert True
    else:
        print("Commit message not as expected")
        print("Last commit message: " + last_commit_message)
        assert False
