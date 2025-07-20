# project - Justfile utility

# Print list of available recipe (this)
default:
    @just --list --unsorted

# Run poetry install in all submodules
install:
    poetry install

# Run the CLI tool with Poetry
testclerk *ARGS:
    @poetry run testclerk {{ ARGS }}

# Build Docker image
build-docker:
    docker build -t project .

# Run CLI through Docker
run-docker:
    docker run --rm -e GITHUB_API_TOKEN="${GITHUB_API_TOKEN}" -e GITHUB_USERNAME="${GITHUB_USERNAME}" project --version

# Run pytest via poetry
pytest *ARGS:
    poetry run pytest {{ ARGS }}

# Run test coverage
coverage:
    poetry run coverage run --source=testclerk --omit="*/__*.py,*/test_*.py,/tmp/*" -m pytest
    poetry run coverage report -m
