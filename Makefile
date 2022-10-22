test:
	poetry run pytest
mypy:
	poetry run mypy .
cl:
	poetry run cz changelog
bump:
	poetry run cz bump --files-only
version: bump
	poetry version $(shell poetry run version)

