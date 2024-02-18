#!/usr/bin/env python3

"""
Python script to handle git commit and push commit messages using conventional commit messages.

Usage: gpush.py
"""

import argparse
import logging
import sys

import inquirer
from git import Repo
from git.exc import GitError

from _version import __version__

VERSION = __version__

# Setup logging


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
    Return the current version of gpush.py.

    Returns:
        String: Current version of gpush.py
    """
    return VERSION


def git_commit(commit_message):
    """
    Commit changes to Git on the current branch for the repository.

    Args:
        commit_message: String containing the conventional commit message formatted commit message

    Raises:
        GitError: If there is an issue with the call to git

    Returns:
        True if commit is successful
    """
    try:
        repo = Repo(search_parent_directories=True)
        repo.index.write()
        repo.git.commit("-m" + commit_message)
        logging.info("committing: %s", commit_message)
        logging.info("Committed successfully")
    except GitError as error_message:
        logging.info("Some error occured while committing the code:")
        logging.info(str(error_message))
        raise
    return True

def print_pr_link(git_response):
    """
    Prints the PR link from the git push response to stdout.

    Args:
        git_response: The response from the git_push function.
    """
    import re
    import validators
    # Explanation: git_response is expected to be a string containing the server's response to a git push command.
    # This response may include a URL to create a new pull request (PR) if the push was successful.
    # Regex pattern to match PR links in git push response
    pr_link_pattern = r"https?://[\w./-]+/pull/\d+"
    if not isinstance(git_response, str) or not validators.url(git_response):
        logging.info("Invalid or missing git response format.")
        return
    try:
        match = re.search(pr_link_pattern, git_response)
    except re.error as regex_error:
        logging.info(f"Error parsing git response with regex: {regex_error}")
        return
    if match:
        print("PR Link: ", match.group())
    else:
        logging.info("No PR link found in the git push response.")


def git_push():
    """
    Push commit up to Git on the current branch for the repository.

    Raises:
        GitError: If there is an issue with the call to git
        Exception: If there is some other issue

    Returns:
        True if push is successful
    """
    try:
        if str(args.branch) != "current":
            branch_name = str(args.branch)
        else:
            repo = Repo(search_parent_directories=True)
            branch_name = repo.active_branch
        repo = Repo(search_parent_directories=True)
        if not repo.heads[branch_name].is_valid():
            repo.create_head(branch_name)
        else:
            logging.info(f"Branch {branch_name} already exists.")
        push_response = repo.git.push("--set-upstream", "origin", branch_name)
        logging.info("Pushed successfully")
        if push_response:
            return push_response
        else:
            logging.info("Push failed, no response received.")
            return None
    except GitError as error_message:
        logging.info("Some error occurred while pushing the code:")
        logging.info(str(error_message))
        raise GitError from error_message
    except Exception as error_message:
        logging.info("Some error occurred while pushing the code:")
        logging.info(str(error_message))
        raise Exception from error_message

    return True


def collect_details():
    """
    Collect commit message detail from the committer and executes git commit and push.

    Raises:
        KeyboardInterrupt: If user exits the script

    Returns:
        commit_message_final: String containing the conventional commit message.
    """
    try:
        questions = [
            inquirer.List(
                "type",
                message="What type of commit is this?",
                choices=["fix", "feat", "docs", "ci", "chore"],
            ),
            inquirer.List(
                "breaking_change",
                message="Does the commit include breaking changes?",
                choices=["Yes", "No"],
            ),
            inquirer.Text(
                "commit_message",
                message="What's your commit message",
            ),
        ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    except KeyboardInterrupt as error_message:
        raise KeyboardInterrupt from error_message

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
    Execute the script.

    Returns:
        True
    """
    if args.version:
        logging.info(get_version())
    else:
        try:
            if args.no_commit:
                if str(args.message) != "None":
                    commit_message = args.message
                else:
                    commit_message = collect_details()
                git_commit(commit_message)
            if args.no_push:
                git_response = git_push()
                if git_response:
                    print_pr_link(git_response)
                else:
                    logging.info("No response from git push, cannot print PR link.")
        except Exception as error_message:
            logging.info("Some error occurred while pushing the code:")
            logging.info(str(error_message))
            sys.exit(1)
        except KeyboardInterrupt:
            logging.info("Okay! Bye!")
            sys.exit(0)
    return True


if __name__ == "__main__":
    main()
