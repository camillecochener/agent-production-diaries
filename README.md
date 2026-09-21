# The Agent Production Diaries

Runnable companion repository for the Medium series *The Agent Production Diaries*.

The repository follows the same fictional product as the articles: CCO AI, an onboarding assistant for Northstar. It is intentionally small. Its purpose is to make production design choices inspectable and testable, not to imitate a complete HR platform.

## What is included today

Chapter 1 contains the product brief and the authority ladder.

Chapter 2 introduces a runnable LangGraph V1 slice with one orchestrator, two skills, six mocked tools, a policy layer, structured traces, and tests for critical access boundaries. It has no model provider or external API dependency and never connects to a real HR or IT system.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

The `.venv` directory is ignored by Git and should not be committed.

## Run a scenario

Python 3.9 or later is the only requirement.

```bash
python3 scripts/run_scenario.py scenarios/chapter-02/missing-laptop.json
```

The command prints the final response and a trace that shows the selected skill, tool call, policy decision, and outcome.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

## Repository map

```text
app/                 The small, dependency free agent harness
docs/                Product, architecture, and tool contract documents
fixtures/            Synthetic approved sources, tasks, and IT requests
medium/              Publishable chapter drafts and visual assets
scenarios/           Reproducible inputs for each chapter
scripts/             Small commands used in the articles
tests/               Permission, handoff, and scenario tests
```

## Important boundary

This repository is educational. The fixtures are synthetic. The request handoff tool creates a draft only. It does not send a ticket, provision access, order equipment, or make an HR decision.

## Copyright and permissions

Copyright © 2026 Camille Cochener. All rights reserved. See [LICENSE.md](LICENSE.md) for the permissions notice.
