#!/usr/bin/env python3

"""
Python script to handle git commit and push to standardise commit messages using conventional commit
messages.

Usage: gpush.py
"""

import argparse

import inquirer
from git import Repo

from _version import __version__

VERSION = __version__

parser = argparse.ArgumentParser(
    prog="gpush " + VERSION,
    description="Git commit helper for conventional commit messages",
)
parser.add_argument(
    "--version", action="store_true", help="Option to print the current version only"
)
parser.add_argument(
    "--no-commit",
    action="store_false",
    help="[Default: False] Option to enable git commit",
)
parser.add_argument(
    "--no-push",
    action="store_false",
    help="[Default: False] Option to enable git push",
)
parser.add_argument(
    "--message",
    action="store",
    help="[Default: None] Override message prompt and use the provided message",
)
parser.add_argument(
    "--branch",
    action="store",
    default="current",
    help="[Default: current] Override using the current branch and use the provided branch",
)


args = parser.parse_args()


def get_version():
    """
    Function to return the current version of gpush.py

    :return: String containing the current version of gpush.py
    """
    return VERSION


def git_commit(commit_message):
    """
    Function to commit changes to Git on the current branch for the repository
    :param commit_message: String containing the conventional commit message formatted commit
    message
    :return: True/False
    """
    try:
        repo = Repo(search_parent_directories=True)
        repo.index.write()
        repo.git.commit("-m" + commit_message)
        print("committing: " + commit_message)
        print("Committed successfully")
    except Exception as error_message:
        print("Some error occured while committing the code:")
        print(str(error_message))
        raise

    return True


def git_push():
    """
    Function to push commit up to Git on the current branch for the repository

    :return: True/False
    """
    try:
        if str(args.branch) != "current":
            branch_name = str(args.branch)
        else:
            repo = Repo(search_parent_directories=True)
            branch_name = repo.active_branch
        repo = Repo(search_parent_directories=True)
        repo.create_head(branch_name)
        repo.git.push("--set-upstream", "origin", branch_name)
        print("Pushed successfully")
    except Exception as error_message:
        print("Some error occurred while pushing the code:")
        print(str(error_message))
        raise

    return True


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

    commit_message_final = (
        answers["type"] + is_breaking_change + ": " + answers["commit_message"]
    )
    return commit_message_final


def main():
    """
    Main function to execute the script
    :return:
    """
    if args.version:
        print(get_version())
    else:
        try:
            if args.no_commit:
                if str(args.message) != "None":
                    commit_message = args.message
                else:
                    commit_message = collect_details()
                git_commit(commit_message)
            if args.no_push:
                git_push()
        except Exception as error_message:
            print("Some error occurred while pushing the code:")
            print(str(error_message))
            raise
    return True


if __name__ == "__main__":
    main()
