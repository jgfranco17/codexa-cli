# Codexa

**Codexa** is a CLI-powered test execution and analysis toolkit that runs your automated tests,
feeds the results into a Large Language Model, and returns actionable, human-friendly insights
for your next development steps.

Think of it as your **post-test intelligence officer** — it doesn't just tell you _what_ failed,
it explains _why_ and _what to do about it_.

---

## Features

- **Config-driven execution**: Define your tests, frameworks, and environments in a single
  configuration file.
- **LLM-powered analysis**: Get context-aware interpretations of failures, flakiness, and
  performance issues.
- **Actionable next steps**: Receive step-by-step recommendations, not just raw logs.
- **Framework-agnostic**: Works with popular testing frameworks (e.g., Pytest, Jest, Go test,
  JUnit) or custom commands.
- **Clear reporting**: Generates concise summaries and detailed diagnostics directly in your
  terminal.

---

## Quick Start

### Install

Install Codexa using `pip`:

```shell
pip install codexa
```

### Configure

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

Codexa uses a YAML configuration file to define:

- Test commands to run
- LLM provider and model
- Output format and destination
- Filters for warnings, failures, and flaky tests

## License

MIT License — see LICENSE for details.
