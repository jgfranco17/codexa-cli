# project - Justfile utility

# Print list of available recipe (this)
_default:
    @just --list --unsorted

# Run poetry install in all submodules
install:
    poetry install
    @echo "Installed dependencies!"

# Run the CLI tool with Poetry
codexa *ARGS:
    @poetry run codexa {{ ARGS }}

# Build Docker image
docker-build:
    docker build -t codexa:0.0.0 .

# Run CLI through Docker
docker-run *ARGS:
    docker run --rm codexa:0.0.0 {{ ARGS }}

# Run pytest via poetry
pytest *ARGS:
    poetry run pytest {{ ARGS }}

# Run test coverage
coverage:
    poetry run coverage run --source=codexa --omit="*/__*.py,*/test_*.py,/tmp/*" -m pytest
    poetry run coverage report -m
