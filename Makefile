lint:
	python3 -m pylint --fail-under=9.5 $$(find . -name "*.py" -not -path "./tests/*")
