from ghapi.all import GhApi
import os
import base64
import shutil
from git import Repo
api = GhApi(token=os.environ.get("GITHUB_TOKEN"))

test_repo_name = "gpush-test"


def create_repo():
    """Create a repository for the authenticated user."""
    repo = api.repos.create_for_authenticated_user(
        name=test_repo_name,
        description="Temporary repo for testing gpush.py, if this repo exists, please delete it.",
        private=True,
    )
    print("Created repo " + test_repo_name)
    return repo


# Create a README file in the repo
def create_readme():
    """Create a README file in the repo."""
    readme = api.repos.create_or_update_file_contents(
        repo=test_repo_name,
        owner=get_user().login,
        path="README.md",
        message="Create README.md",
        content=base64.b64encode("This is a temporary repo for testing gpush.py, if this repo exists, please delete it.".encode("ascii")).decode("ascii"),
    )
    print("Created README in repo " + test_repo_name)
    return readme

def get_user():
    """Get the authenticated user."""
    user = api.users.get_authenticated()
    return user


def delete_repo():
    """Delete a repository for the authenticated user."""
    repo = api.repos.delete(
        repo=test_repo_name,
        owner=get_user().login,
    )
    print("Deleted repo " + test_repo_name)
    return repo

def cleanup_local():
    """Cleanup local files."""
    if os.path.exists(test_repo_name):
        shutil.rmtree(test_repo_name)
        print("Deleted local directory " + test_repo_name)
    else:
        print("The directory " + test_repo_name + " does not exist")
    return True

def create_branch():
    """Create a branch on a repo."""
    print("Creating branch " + test_repo_name)
    repo = api.repos.create_branch(
        repo=test_repo_name,
        owner=get_user().login,
        branch="test-branch",
    )
    print("Cloned repo " + test_repo_name)
    return repo

# Use python git to clone repository
def clone_repo():
    """Clone the repository."""
    print("Cloning repo " + test_repo_name)
    Repo.clone_from("https://github.com/tjtharrison/gpush-test.git", "gpush-test")

    return True

if __name__ == "__main__":
    try:
        create_repo()
        print("Repo created successfully")
    except Exception as error_message:
        print("Some error occurred while creating the repo:")
        print(str(error_message))
        raise

    try:
        delete_repo()
        print("Repo deleted successfully")
    except Exception as error_message:
        print("Some error occurred while deleting the repo:")
        print(str(error_message))
        raise