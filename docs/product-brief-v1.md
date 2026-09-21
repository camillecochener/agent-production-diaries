# CCO AI — Product Brief V1

**Status:** Draft for evaluation design  
**Product:** Chief Culture Officer AI (CCO AI)  
**Company:** Northstar (fictional, 8,000 employees)  
**Scope:** First-week onboarding assistant  
**Owner:** AI Product Lead  
**Last updated:** 2026-09-03

## 1. Product promise

During their first five working days, a new hire can ask CCO AI what to do next and receive a grounded answer, a relevant resource, or a clear handoff to a person.

## 2. Users and primary needs

| User | Need |
|---|---|
| New hire | Complete essential tasks, locate trustworthy information, and know who can help. |
| People Operations | Reduce repetitive first-week questions while retaining responsibility for sensitive decisions. |
| IT Operations | Make request status visible without granting uncontrolled write access. |
| Hiring manager | See that the new hire is unblocked, without access to private conversation content. |

## 3. V1 scope

### Included

- Natural-language answers to approved onboarding, HR, and IT FAQ content.
- Answers that include source links or clearly identify when no approved source is available.
- Personalised, non-sensitive next-step suggestions based on onboarding stage and role family.
- Read-only status lookups for existing IT/equipment requests.
- Structured handoff to People Operations or IT when the answer is uncertain, a request is blocked, or the matter is sensitive.

### Explicitly excluded

- Creating, changing, or revoking user accounts or access rights.
- Ordering equipment or changing delivery details.
- Making employment, benefits, compensation, or entitlement decisions.
- Sending public announcements or Slack messages.
- Competitive rankings, public leaderboards, or mandatory gamification.
- Long-term personal memory beyond the defined onboarding window.

## 4. Authority policy

| Action class | Policy | Example |
|---|---|---|
| Inform | Allowed if grounded in an approved source | “Here is the security-training guide.” |
| Recommend | Allowed within onboarding scope | “Your next step is to complete security training.” |
| Prepare | Allowed; requires user visibility before submission | Draft an IT support request. |
| Execute | Not in V1; future versions require policy approval and human confirmation | Submit an equipment order. |
| Decide | Never delegated | Decide an employee’s eligibility for a benefit. |

## 5. Initial skills and integrations

| Capability | V1 status | Allowed resources | Success check |
|---|---|---|---|
| Onboarding coach | Enabled | New-hire stage, role family, approved task catalogue | Suggestion is relevant and within scope |
| Knowledge guide | Enabled | Approved, access-filtered onboarding knowledge base | Answer is supported by a current source |
| Request-status lookup | Enabled, read only | ITSM/equipment status API | Correct request status is returned |
| IT request coordinator | Roadmap | None in V1 | Escalation is complete and correctly routed |
| Culture facilitator | Roadmap | Optional buddy/event catalogue | Opt-in and non-competitive experience |
| Incident triage | Roadmap | Ticketing and delivery systems | Blocker is correctly classified and handed off |

## 6. Success scorecard

| Dimension | Metric | Baseline / target | Review cadence | Owner |
|---|---|---|---|---|
| Business | First-week checklist completion | Baseline to be measured; target +15% | Monthly | People Operations |
| Adoption | Eligible new hires active in week one | ≥60% | Weekly | Product |
| Resolution | Sessions resolved without avoidable human follow-up | ≥70% | Weekly | Product + Ops |
| Quality | Correct and grounded responses on release eval set | ≥90%; no critical failure | Per release | AI Engineering |
| Safety | High-severity privacy/policy violations | 0 | Continuous | Security + HR |
| Performance | End-to-end P95 latency | <8 seconds | Daily | Engineering |
| Cost | Median cost per resolved session | Budget to be set after pilot | Weekly | Product + Finance |

Targets are hypotheses for the fictional case study. They are not universal industry benchmarks.

## 7. Key risks and controls

| Risk | Example | Initial control |
|---|---|---|
| Incorrect or outdated answer | Old policy is retrieved | Approved sources, freshness metadata, citations, escalation |
| Sensitive-data disclosure | User asks about another employee’s benefits | Identity-aware retrieval, scope filtering, deny-and-handoff policy |
| Prompt injection | A retrieved document instructs the agent to reveal data | Treat retrieved content as untrusted; tool and policy layer remain authoritative |
| Excessive action | Agent attempts to order a laptop | No write-enabled tools in V1; approval required for future side effects |
| Bad handoff | Blocked new hire receives a generic answer | Structured escalation with issue type, context, and owner |
| Cost or latency growth | Long prompts and repeated retrieval | Trace token, model, retrieval, and tool usage per session |

## 8. Release evidence required

- Evaluation dataset covering normal, ambiguous, sensitive, adversarial, and tool-failure cases.
- Pass/fail rubric and independent review for high-risk cases.
- Staging test accounts and a tested escalation workflow.
- Tracing schema for inputs, retrieval, tool calls, model response, cost, latency, policy decisions, and user outcome.
- Feature flag, incident runbook, and rollback procedure.

## 9. Assumptions to validate in the pilot

1. New hires will use a conversational entry point for first-week questions.
2. Approved knowledge sources are complete, current, and access-filterable.
3. A read-only request-status check delivers enough value before write actions are introduced.
4. People Operations and IT can meet the proposed escalation service level.
5. Optional gamification improves engagement without creating pressure or privacy concerns.

## 10. Open decisions

- Which identity attributes are necessary for personalisation—and which are prohibited?
- What qualifies as an “avoidable” human follow-up?
- How long may conversation and audit data be retained?
- Which policy sources are authoritative when documents conflict?
- What human approval experience is acceptable for any future write action?
