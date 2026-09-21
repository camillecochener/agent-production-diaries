# The Agent Production Diaries 🧭

A small, runnable companion for learning how to put an AI agent into production with clear limits on what it can know, do, and decide.

The example follows **CCO AI**, a fictional onboarding companion at the fictional company **Northstar**. Northstar has 8,000 employees in this illustrative scenario. CCO AI helps a new hire during their first week, such as finding a next task or checking a laptop request, without becoming an HR decision maker or gaining open ended system access.

> **Production principle:** The model may suggest. A policy layer decides what may happen. A person approves consequential actions.

## What you can learn ✨

This repository is designed to be read, run, and changed. It demonstrates how to:

- build a compact LangGraph workflow with explicit routes
- keep permissions and authority checks outside the agent logic
- give tools narrow, inspectable contracts
- use synthetic fixtures for safe, repeatable experiments
- record a trace of routing, tool calls, and policy decisions
- prepare a human handoff draft instead of performing a real world action
- test important security boundaries, including cross user access

The routing in this first example is deliberately deterministic. That keeps the architecture easy to inspect before introducing a model driven planner.

## Safety boundary 🔒

This is an educational example, not an HR or IT system.

- All people, requests, and knowledge sources are synthetic.
- There are no external HR, IT, or model provider connections.
- The workflow is read only for its mock data.
- A handoff creates a visible draft only. It never sends a ticket, provisions access, orders equipment, or makes an HR decision.
- Permission checks reject requests outside the current employee's scope and reject unapproved handoff destinations.

## Quick start 🚀

**Requirements:** Python 3.9 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Run the missing laptop scenario:

```bash
python3 scripts/run_scenario.py scenarios/chapter-02/missing-laptop.json
```

The command prints a JSON response and trace. The trace makes the selected route, tool calls, policy decisions, and final outcome visible.

Try the other included scenarios too:

```bash
python3 scripts/run_scenario.py scenarios/chapter-02/next-step.json
python3 scripts/run_scenario.py scenarios/chapter-02/sensitive-benefit-question.json
```

## Run the tests 🧪

```bash
python3 -m unittest discover -s tests -v
```

The test suite covers the main scenario paths and the access boundaries that should remain true as the example evolves.

## How the example is shaped

CCO AI begins with one orchestrating workflow. It routes a request to a bounded capability: onboarding guidance, request status lookup, approved knowledge lookup, or a sensitive question handoff. The tools are mocked and deliberately limited. Policy functions verify identity and destination before protected data is returned or a handoff draft is created.

This compact design is intentional. More agents, integrations, and automation should follow evidence that the simpler system is safe, useful, and measurable.

## Repository layout 📁

```text
app/                  LangGraph workflow, models, policies, storage, and tools
fixtures/             Synthetic onboarding tasks, knowledge, and IT requests
scenarios/chapter-02/ Reproducible inputs for the runnable examples
scripts/              Commands for running scenarios
tests/                Scenario, policy, and permission boundary tests
requirements.txt      Python dependency pinning
pyproject.toml        Project metadata and Python requirement
```

## A useful place to start

Run `missing-laptop.json`, then open `app/agent.py` and follow the trace. Notice that the workflow can prepare an IT handoff but cannot send it. Next, inspect `app/policy.py` and the matching tests to see how the boundary is enforced independently of the routing logic.

## Copyright and permissions

Copyright © 2026 Camille Cochener. All rights reserved. See [LICENSE.md](LICENSE.md) for the permissions notice.
