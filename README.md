# gpush

`gpush` is a command line utility for standardising commit messages using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). It is designed to be used in conjunction with [semantic-release](https://semantic-release.gitbook.io/semantic-release/usage/configuration) to automate the release of your package based on commits that are made on a branch when a PR is merged.

## Signing commits

`gpush` natively supports signing commits using GPG. To enable this, you will need to have GPG installed and configured on your machine. You can find instructions on how to do this [here](https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification/generating-a-new-gpg-key).

# Installation

This package is available for installation via git. To install the latest version, run the following command:

```
pip3 install git+https://github.com/tjtharrison/gpush.git
```

# Usage

When running gpush in a git directory, use `gpush` to replace your standard `git commit && git push` commands. `gpush` will ask a few questions to determine detail about your commit and generate a conventionally formatted git commit message.

## Example

!["gpush_demo"](docs/gpush_demo.gif)

To see additional options available, run gpush with the  `--help` flag

```
gpush --help
```

# Local development

To develop locally, uninstall any existing version of gpush before executing the pip3 installation in the local directory, use Makefile command to do this:

```
make dev
```

# Unit tests

To run unit tests, execute the following command, you will need to have pytest installed and set environment variable `GITHUB_TOKEN` to a valid GitHub token that has permissions to create/delete and push to a repository within your account.

```
make test
```

The unit tests will create a test repository within your account for each unit test before testing functionality and deleting the repository.
