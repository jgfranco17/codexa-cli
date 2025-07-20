# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

LABEL maintainer="Chino Franco <chino.franco@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.5

RUN apt-get update && apt-get install -y \
        --no-install-recommends \
        curl \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY README.md pyproject.toml poetry.lock* ./
COPY testclerk ./testclerk
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main \
    && poetry build \
    && pip install dist/*.whl

ENTRYPOINT ["testclerk"]
CMD ["--help"]
