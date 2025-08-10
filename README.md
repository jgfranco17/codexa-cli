# Codexa

**Codexa** is a CLI-powered test execution and analysis toolkit that runs your automated tests,
feeds the results into a Large Language Model, and returns actionable, human-friendly insights
for your next development steps.

Think of it as your **post-test intelligence officer** — it doesn't just tell you _what_ failed,
it explains _why_ and _what to do about it_.

## Why Codexa?

Test automation is a critical part of modern software development. It helps catch bugs early,
ensures code quality, and streamlines the development process. However, the sheer volume of
automated tests can be overwhelming, and the results can be difficult to interpret. Codexa aims
to bridge the gap between raw test results and clear, actionable insights.

It blends two conceptual roots:

- _Code_: The foundation. Codexa works directly with the output of your code's test suite,
  parsing and understanding raw results.
- _Lexa_: From _lexis_ (Greek for "word" or "speech") and lexicon (the vocabulary of a language).
  This evokes the language-focused intelligence of the tool — it doesn't just run tests, it
  speaks about them in a clear, actionable way.

In essence, Codexa is the bridge between raw code execution and clear human insight.

## Features

Codexa provides a powerful set of features to help you analyze your test results.

- **Config-driven execution**: Define your tests, frameworks, and environments in a single
  configuration file.
- **LLM-powered analysis**: Get context-aware interpretations of failures, flakiness, and
  performance issues.
- **Actionable next steps**: Receive step-by-step recommendations, not just raw logs.
- **Framework-agnostic**: Works with popular testing frameworks (e.g., Pytest, Jest, Go test,
  JUnit) or custom commands.
- **Clear reporting**: Generates concise summaries and detailed diagnostics directly in your
  terminal.

This brings the power of Codexa to your terminal, empowering you to make informed decisions
about your code's quality and performance.

---

## Quick Start

### Install

Install Codexa using `pip`:

```shell
pip install codexa
```

### Configure

Codexa uses a YAML configuration file to define:

- Test commands to run
- LLM provider and model
- Output format and destination
- Filters for warnings, failures, and flaky tests

```yaml filename=".codexa.yaml"
tests:
  - id: python
    command: pytest --maxfail=1 --disable-warnings
  - id: javascript
    command: npm test -- --maxWorkers=1
  - id: go
    command: go test -v -timeout 30s

llm:
  provider: openai
  model: gpt-4o
  api_key: $OPENAI_API_KEY
```

### Run

Codexa will automatically detect your configuration file and execute the tests defined within
it. It will then analyze the results using the specified LLM provider and model.

```shell
codexa run
```

## License

MIT License — see LICENSE for details.
