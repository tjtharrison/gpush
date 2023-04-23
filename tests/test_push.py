import pytest
import tests.bin.github as github
from gpush import git_commit
import subprocess


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


def test_git_push_only():
    """
    Function to test the git_commit function in gpush.py with no-commit.
    :return:
    """
    try:
        commands = [
            "cd gpush-test",
            "git checkout -b test-branch",
        ]
        ret = subprocess.run(";".join(commands), capture_output=True, shell=True)
        print("Branch setup locally")
    except Exception as error_message:
        print("Some error occurred while setting up the branch locally")
        print(str(error_message))
        raise

    try:
        commands = [
            "cd gpush-test",
            "touch test-push",
            "git add test-push",
            "git commit -m \"Test manual commit\"",
            "../gpush.py --no-commit",
        ]
        ret = subprocess.run(";".join(commands), capture_output=True, shell=True)
        print("Code pushed successfully")
    except Exception as error_message:
        print("Some error occurred while committing to the branch locally")
        print(str(error_message))
        raise

    try:
        last_commit_message = github.get_last_commit_message("test-branch")
    except Exception as error_message:
        print("Some error occurred while getting the last commit message")
        print(str(error_message))
        raise

    if last_commit_message == "Test manual commit":
        assert True
    else:
        print("Commit message not as expected")
        print("Last commit message: " + last_commit_message)
        assert False


def test_git_push_only_custom_branch():
    """
    Function to test the git_commit function in gpush.py with no-commit and specifying custom branch.
    :return:
    """
    try:
        commands = [
            "cd gpush-test",
            "git checkout -b test-branch",
        ]
        ret = subprocess.run(";".join(commands), capture_output=True, shell=True)
        print("Branch setup locally")
    except Exception as error_message:
        print("Some error occurred while setting up the branch locally")
        print(str(error_message))
        raise

    try:
        commands = [
            "cd gpush-test",
            "touch test-push",
            "git add test-push",
            "git commit -m \"Test manual commit\"",
            "../gpush.py --no-commit --branch test-branch-2",
        ]
        ret = subprocess.run(";".join(commands), capture_output=True, shell=True)
        print("Code pushed successfully")
    except Exception as error_message:
        print("Some error occurred while committing to the branch locally")
        print(str(error_message))
        raise

    try:
        last_commit_message = github.get_last_commit_message("test-branch-2")
    except Exception as error_message:
        print("Some error occurred while getting the last commit message")
        print(str(error_message))
        raise

    if last_commit_message == "Test manual commit":
        assert True
    else:
        print("Commit message not as expected")
        print("Last commit message: " + last_commit_message)
        assert False
