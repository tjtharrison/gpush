# gpush

Script for standardising commit messages on git push using "Conventional commit" format. The package handles GPG signing for commits out of the box (using your local git configuration)

https://www.conventionalcommits.org/en/v1.0.0/

# Installation

This package is available for installation via pypi

```
pip3 install gpush
```

# Configuration

To start using gpush, run the following (update as required if you do not use zsh)

```
echo "alias gpush=\"python3 -m gpush\"" >> ~/.zshrc
```

To start using straight away, source your file

```
source ~/.zshrc
```
