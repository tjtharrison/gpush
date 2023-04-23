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

# Use python git to clone repository
def clone_repo():
    """Clone the repository."""
    print("Cloning repo " + test_repo_name)
    Repo.clone_from("https://github.com/tjtharrison/gpush-test.git", "gpush-test")

    return True

# Function to get the last commit from the github api
def get_last_commit_message(branch_name):
    """Get the last commit from the github api.
    :param branch_name: The name of the branch to get the last commit from.
    :return: The last commit message.
    """
    last_commit = api.repos.get_commit(
        repo=test_repo_name,
        owner=get_user().login,
        ref=branch_name,
    )
    return last_commit["commit"]["message"]
