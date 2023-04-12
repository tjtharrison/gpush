from ghapi.all import GhApi
import os

api = GhApi(token=os.environ.get("GITHUB_TOKEN"))

test_repo_name = "gpush.py-test"


def create_repo():
    """Create a repository for the authenticated user."""
    repo = api.repos.create_for_authenticated_user(
        name=test_repo_name,
        description="TEMPORARY repo for testing gpush.py, if this repo exists, please delete it.",
        private=True,
    )
    return repo


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
    return repo


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
