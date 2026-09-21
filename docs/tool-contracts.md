# CCO AI V1 Tool Contracts

Every tool has a narrow purpose, explicit permission checks, a defined failure response, and fields that must be retained in a trace.

| Tool | Purpose | Authority | Validated outside the model | Trace fields | Failure behaviour |
|---|---|---|---|---|---|
| `get_onboarding_checklist` | Return the authenticated user’s first week tasks | Inform | Employee identity and onboarding stage | User, checklist version, result count | Explain that the list is unavailable and offer handoff |
| `get_onboarding_task_detail` | Return approved instructions for one task | Inform | Task identifier and user access | Task identifier, source version | Do not invent instructions |
| `search_approved_knowledge` | Search approved onboarding content | Inform | Search scope and source permission | Query, source identifiers, ranking | State that no approved answer was found |
| `get_approved_source` | Retrieve an approved source passage | Inform | Source permission and version | Source identifier, publication date | Do not use inaccessible or stale sources |
| `get_it_request_status` | Read a user’s existing IT request status | Inform | Request ownership and identity | Request identifier, status | Offer IT handoff if status is unavailable |
| `prepare_human_handoff` | Create a user visible escalation draft | Prepare | Destination, issue class, user identity | Destination, issue class, draft identifier | Never claim that a ticket was sent |

## Contract rules

1. The model does not decide whether it has access. Policy code does.
2. Read access is scoped to the authenticated user and approved sources.
3. A failed tool call is a product state. The system must explain the limitation or hand off.
4. A prepare tool is not an execute tool. It returns a draft and has no external side effect.
5. Tool inputs and outputs are part of the trace, subject to the data retention policy of a real deployment.
