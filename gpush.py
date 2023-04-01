from git import Repo
import inquirer
import sys

questions = [
    inquirer.List(
        "type",
        message="What type of commit is this?",
        choices=["fix", "feat", "docs", "ci"],
    ),
    inquirer.List(
        "breaking_change",
        message="Does the commit include breaking changes?",
        choices=["Yes","No"],
    ),
    inquirer.Text('commit_message', message="What's your commit message"),
]

answers = inquirer.prompt(questions)
if answers["breaking_change"] == "Yes":
    is_breaking_change = "!"
else:
    is_breaking_change = ""

commit_message = answers["type"] + is_breaking_change + ": " + answers["commit_message"]

def git_push():
    try:
        repo = Repo(sys.argv[1])
        repo.git.add(update=True)
        repo.index.commit(commit_message)
        repo.git.push('--set-upstream', 'origin', repo.active_branch)
    except Exception as error_message:
        print('Some error occured while pushing the code:')
        print(str(error_message))

git_push()
