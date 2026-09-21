# CCO AI V1 Architecture

CCO AI V1 is a small LangGraph workflow. Its shared state records the actor, message, selected route, trace, response, and outcome. The routing node selects a skill. Deterministic application code then validates permissions before any tool receives an input.

```text
New hire
  to CCO AI orchestrator
      to onboarding coach
          to onboarding checklist tools
      to knowledge guide
          to approved knowledge tools
      to request status lookup
          to IT request status tool
      to human handoff draft
  to source backed answer, next step, status, or handoff draft
```

## Design decisions

| Decision | Rationale |
|---|---|
| LangGraph StateGraph | The graph makes routes, nodes, state, and terminal outcomes explicit and testable. |
| One orchestrator | V1 is easier to test and trace before separate agents are justified. |
| Two active skills | The onboarding coach and knowledge guide map to distinct user outcomes. |
| Read only system access | The system can inspect approved data but cannot change downstream records. |
| Handoff drafts only | A user can review the proposed escalation before any person receives it. |
| Fixture backed tools | Readers can run scenarios without credentials or sensitive data. |
| Structured traces | Every response records skill choice, tool use, policy result, and outcome. |

## What this architecture does not claim

The deterministic routing node in this repository is a test harness, not a production language model. In a later chapter, a model backed planner can replace that one graph node while the policy checks, tool contracts, fixtures, scenarios, and tests remain in place.
