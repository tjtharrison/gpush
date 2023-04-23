lint:
	python3 -m pylint --fail-under=9.5 $$(find . -name "*.py" -not -path "./tests/*")

test:
	python3 -m pytest

dev:
	pip3 uninstall gpush
	pip3 install -e .
