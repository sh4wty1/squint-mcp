# Contributing to Squint

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Before you open a pull request

All four must pass. CI runs the same commands.

```bash
uv run pyright              # typecheck (strict)
uv run ruff check           # lint
uv run ruff format --check  # format check (run `uv run ruff format` to fix)
uv run pytest               # tests
```

## Tests

Tests have one seam: the MCP tool boundary. They connect an in-memory MCP client to the server, call tools, and assert on what comes back. Do not add unit tests for internal helpers; cover them through a tool. The reasoning is in [`docs/SPEC.md`](docs/SPEC.md), under Testing Decisions.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `feat(ping): ...`, `fix: ...`, `docs: ...`. Keep commits small.

## Language

Everything public is in English: code, comments, documents, commit messages, and the messages Squint returns.

Use the vocabulary in [`CONTEXT.md`](CONTEXT.md). A Check yields Findings from a Capture; avoid "detector", "rule", "issue" and "screenshot" for those concepts.

## Changelog

Add an entry under `Unreleased` in [`CHANGELOG.md`](CHANGELOG.md) for any change a user can observe. New Checks and threshold changes always get an entry.
