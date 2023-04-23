"""
Collection of functions to interact with the github api.
"""

import base64
import os
import shutil

from ghapi.all import GhApi
from git import Repo

api = GhApi(token=os.environ.get("GITHUB_TOKEN"))

TEST_REPO_NAME = "gpush-test"


def create_repo():
    """Create a repository for the authenticated user.
    :return: The created repository"""
    repo = api.repos.create_for_authenticated_user(
        name=TEST_REPO_NAME,
        description="Temporary repo for testing gpush.py, if this repo exists, please delete it.",
        private=True,
    )
    print("Created repo " + TEST_REPO_NAME)
    return repo


# Create a README file in the repo
def create_readme():
    """Create a README file in the repo.
    :return: The created file"""
    readme = api.repos.create_or_update_file_contents(
        repo=TEST_REPO_NAME,
        owner=get_user().login,
        path="README.md",
        message="Create README.md",
        content=base64.b64encode(
            "Temporary repo for testing gpush.py, if this repo exists, please delete it.".encode(
                "ascii"
            )
        ).decode("ascii"),
    )
    print("Created README in repo " + TEST_REPO_NAME)
    return readme


def get_user():
    """Get the authenticated user.
    :return: The authenticated user
    """
    user = api.users.get_authenticated()
    return user


def delete_repo():
    """Delete a repository for the authenticated user.
    :return: The deleted repository
    """
    repo = api.repos.delete(
        repo=TEST_REPO_NAME,
        owner=get_user().login,
    )
    print("Deleted repo " + TEST_REPO_NAME)
    return repo


def cleanup_local():
    """Cleanup local files.
    :return: True
    """
    if os.path.exists(TEST_REPO_NAME):
        shutil.rmtree(TEST_REPO_NAME)
        print("Deleted local directory " + TEST_REPO_NAME)
    else:
        print("The directory " + TEST_REPO_NAME + " does not exist")
    return True


# Use python git to clone repository
def clone_repo():
    """Clone the repository.
    :return: True"""
    print("Cloning repo " + TEST_REPO_NAME)
    Repo.clone_from("https://github.com/tjtharrison/gpush-test.git", "gpush-test")

    return True


# Function to get the last commit from the github api
def get_last_commit_message(branch_name):
    """Get the last commit from the github api.
    :param branch_name: The name of the branch to get the last commit from.
    :return: The last commit message.
    """
    last_commit = api.repos.get_commit(
        repo=TEST_REPO_NAME,
        owner=get_user().login,
        ref=branch_name,
    )
    return last_commit["commit"]["message"]
