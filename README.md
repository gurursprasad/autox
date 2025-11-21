# autox

A versatile test-automation and deployment CLI for running UI/API tests,
provisioning environments, and automating QA workflows.

## Features

- Command-line interface for running test suites (`autox` console script).
- Runs UI tests (Selenium / Playwright) and API tests via `pytest`.
- Generates HTML reports and JUnit XML output for CI ingestion.
- Centralized configuration via environment variables and `autox.config`.
- Built-in logging with per-run log folders under `autox_logs/`.

## Requirements

- Python 3.12 or later
- Recommended: virtualenv or pyenv for isolated environments

The main runtime dependencies are declared in `pyproject.toml`.

## Installation

Clone the repository and install in editable mode:

```bash
git clone <repo_url>
cd autox
python -m venv .venv

# Install poetry via pip
pip install poetry
poetry install
```

Install developer tools (linters, docs, test extras) as needed using your preferred method.

After installation, the `autox` console script is available:

```bash
autox --help
```

## Configuration

`autox` reads configuration from environment variables. Common keys are defined
in `autox/config.py` (via `ConfigMap`). Useful variables:

- `APP_URL` — application UI base URL
- `API_URL` — base URL for API tests
- `API_KEY` — API key for authenticated tests
- `LOG_LEVEL` — logging level (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `AWS_REGION`, `AWS_ACCOUNT_ID`, `EKS_CLUSTER_NAME` — cloud infra values
- `GITHUB_TOKEN`, `GITHUB_REPO_OWNER` — for automation that talks to GitHub
- `TF_GITHUB_REPO`, `TF_GITHUB_BRANCH` — terraform repository settings

You can create a `.env` file or export environment variables in your shell:

```bash
export LOG_LEVEL=INFO
export API_URL=https://api.example.local
```

## Usage

The package exposes a Click-based CLI. The primary entrypoint is the `autox` script
installed by the package (see `[project.scripts]` in `pyproject.toml`). Examples:

- Show help and available commands:

```bash
autox --help
```

- Run the UI test group (example):

```bash
# Note: the CLI defines a group named `run-ui-tests` with a subcommand also named
# `run-ui-tests` (so the invocation currently is two parts). You can also run pytest directly.
autox run-ui-tests --browser chrome --headless
```

- Run the API tests via the CLI:

```bash
autox run-api-tests
```

- Or run tests directly with `pytest` (same options apply):

```bash
pytest -v -s --html=report.html --self-contained-html --junitxml=results/test-results.xml tests/ui_tests
pytest -v -s --html=report.html --self-contained-html --junitxml=results/test-results.xml tests/api_tests
```

The test runner writes `report.html` and `results/test-results.xml` by default.

## Logging and Reports

- Per-run logs are created under `autox_logs/run-<timestamp>/autox_logs.log`.
- HTML test report is `report.html` in the repository root (overwritten each run).
- JUnit XML is written to `results/test-results.xml` for CI integration.

## Troubleshooting

- If tests fail with browser issues, ensure webdriver binaries are available
	(this project can use `webdriver-manager` / Playwright to provision drivers).
- If logging is noisy, set `LOG_LEVEL=INFO` or `WARNING` before running.

## License

This project is licensed under the MIT License (see `LICENSE`).
