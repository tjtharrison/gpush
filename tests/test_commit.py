import pytest
import tests.bin.github as github
from gpush import git_commit

@pytest.fixture(autouse=True)
def my_fixture():
    """
    Wrapper for config unit tests to back up and restore configuration to test field manipulation.
    :return:
    """
    github.create_repo()
    yield
    github.delete_repo()
    github.cleanup_local()

def test_git_commit():
    """
    Function to test the git_commit function in gpush.py
    :return:
    """
    try:
        github.create_readme()
        github.clone_repo()
    except Exception as error_message:
        print("Some error occurred while creating README:")
        print(str(error_message))
        raise


    # try:
    #     github.create_branch()
    #     git_commit("test: test commit")
    # except Exception as error_message:
    #     print("Some error occurred while committing the code:")
    #     print(str(error_message))
    #     raise
    assert False
