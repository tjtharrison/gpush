"""
Python script to handle git commit and push to standardise commit messages using conventional commit
messages.

Usage: gpush
"""

import inquirer
from git import Repo


def git_push(commit_message):
    """
    Function to push commit up to Git on the current branch for the repository
    :param commit_message: String containing the conventional commit message formatted commit
    message
    :return: True/False
    """
    try:
        repo = Repo(search_parent_directories=True)
        repo.index.write()
        repo.git.commit('-m "' + commit_message + '"')
        repo.git.push("--set-upstream", "origin", repo.active_branch)
        print("pushing commit: " + commit_message)
        print("Pushed successfully")
    except Exception as error_message:
        print("Some error occured while pushing the code:")
        print(str(error_message))


def collect_details():
    """
    Function that collects commit message detail from the committer and executes git commit
    and push.

    :return: True/False
    """
    questions = [
        inquirer.List(
            "type",
            message="What type of commit is this?",
            choices=["fix", "feat", "docs", "ci"],
        ),
        inquirer.List(
            "breaking_change",
            message="Does the commit include breaking changes?",
            choices=["Yes", "No"],
        ),
        inquirer.Text("commit_message", message="What's your commit message"),
    ]

    answers = inquirer.prompt(questions)
    if answers["breaking_change"] == "Yes":
        is_breaking_change = "!"
    else:
        is_breaking_change = ""

    commit_message = (
        answers["type"] + is_breaking_change + ": " + answers["commit_message"]
    )
    git_push(commit_message)


if __name__ == "__main__":
    collect_details()
