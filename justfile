# project - Justfile utility

# Print list of available recipe (this)
_default:
    @just --list --unsorted

# Run poetry install in all submodules
install:
    poetry install
    @echo "Installed dependencies!"

# Run the CLI tool with Poetry
testclerk *ARGS:
    @poetry run testclerk {{ ARGS }}

# Build Docker image
docker-build:
    docker build -t testclerk:0.0.0 .

# Run CLI through Docker
docker-run *ARGS:
    docker run --rm testclerk:0.0.0 {{ ARGS }}

# Run pytest via poetry
pytest *ARGS:
    poetry run pytest {{ ARGS }}

# Run test coverage
coverage:
    poetry run coverage run --source=testclerk --omit="*/__*.py,*/test_*.py,/tmp/*" -m pytest
    poetry run coverage report -m

# Run BDD tests with Behave
behave *ARGS:
    poetry run behave {{ ARGS }}

bdd-dry-run:
    poetry run behave --dry-run

# Run type checking on BDD tests
type-check:
    poetry run mypy features/

# Run type checking with strict mode
type-check-strict:
    poetry run mypy --strict features/

# Run all checks (tests + type checking)
check-all:
    poetry run pytest
    poetry run behave
    poetry run mypy features/
