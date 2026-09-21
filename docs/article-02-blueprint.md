# Chapter 2 Blueprint: One Agent, Six Tools, and Clear Boundaries

## Purpose in the series

Chapter 1 defined the product promise, authority boundary, risks, and release evidence for CCO AI. Chapter 2 turns that contract into a deliberately small technical design.

The chapter demonstrates a central production principle: a tool is not a capability to showcase. It is a permission the system must earn, describe, test, and observe.

## Working title and subtitle

**Title:** One Agent, Six Tools, and Clear Boundaries  
**Subtitle:** How to design skills and tool contracts before an AI system earns the right to act

## Reader promise

By the end of the chapter, the reader can:

1. Split an agentic use case into a small number of bounded skills.
2. Write a tool contract that is safe, testable, and observable.
3. Choose tool permissions based on authority and reversibility.
4. Handle missing information and tool failure without pretending the system succeeded.
5. Identify the evidence that would justify adding more tools or separate agents.

## Opening scene

Maya presents the V1 product brief to Priya, who leads IT Operations. Priya agrees that the assistant may help Leo find information. Then she asks one question: “Which systems will it be able to change?”

The room becomes quiet. The design is no longer a chat experience. It is a list of permissions, interfaces, failure modes, and accountable owners.

The narrator introduces the idea of the chapter:

> An agent becomes operational when it crosses a boundary. Tools are those boundaries.

## The V1 system

CCO AI has one LangGraph `StateGraph` orchestrator and two enabled skills. Graph state records the actor, message, selected skill, trace, response, and outcome. The routing node chooses the next skill, but application policy controls access and validates all tool arguments.

```text
New hire
  to CCO AI orchestrator
      to onboarding coach
          to get onboarding checklist
          to get onboarding task detail
      to knowledge guide
          to search approved knowledge
          to get approved source
      to request status lookup
          to get IT request status
      to escalation draft
          to prepare human handoff
  to answer with source, next step, or explicit handoff
```

The system uses six tools. Five read information or prepare a draft. None executes a consequential action. The graph provides explicit nodes and conditional routes, while tools and policy code remain framework independent.

## The six tool contracts

| Tool | Purpose | Authority | Inputs validated outside the model | Output to retain in trace | Failure response |
|---|---|---|---|---|---|
| `get_onboarding_checklist` | Return the current task list for the authenticated new hire | Inform | Employee identity, onboarding stage | Checklist version and access decision | Explain that the task list is unavailable and offer People Operations handoff |
| `get_onboarding_task_detail` | Return the source and instructions for one task | Inform | Task identifier, user access | Source identifier and freshness date | Do not invent instructions; show escalation path |
| `search_approved_knowledge` | Search approved onboarding sources | Inform | Search scope, user access, source permissions | Retrieved source identifiers and ranking | State that no approved answer was found |
| `get_approved_source` | Retrieve the selected source passage and metadata | Inform | Source permission, version | Source version, publication date | Do not answer from stale or inaccessible content |
| `get_it_request_status` | Read the status of the user’s existing IT request | Inform | Request ownership and identity | Request identifier, returned status | State that status is unavailable and offer IT handoff |
| `prepare_human_handoff` | Create a user visible draft for People Operations or IT | Prepare | Destination, issue type, user confirmation | Handoff category and draft contents | Keep the conversation open; do not claim a ticket was sent |

## Chapter structure

### 1. A tool is an authority boundary

Explain the difference between a prompt instruction and an integration that can access data or create a side effect. Establish the rule that the model never validates its own access.

Introduce the tool contract. Each tool needs purpose, input validation, output schema, permission checks, timeouts, failure behaviour, trace fields, and an owner.

### 2. Design skills around user outcomes

Define the two active skills:

| Skill | Job | May use | May not do | Success signal |
|---|---|---|---|---|
| Onboarding coach | Provide the next relevant first week step | Checklist and task detail tools | Interpret a sensitive policy or execute a task | Suggested step is relevant and the user can complete it |
| Knowledge guide | Answer a question using an approved source | Search and source tools | Answer without source support | Answer is accurate, relevant, and cited |

Explain why request status and escalation are supporting capabilities rather than separate agents in V1.

### 3. The request lifecycle

Walk through three interactions:

1. A straightforward question: Leo asks what to do after security training. The onboarding coach retrieves the current checklist and task detail, then gives one source linked next step.
2. A blocked user: Leo asks where his laptop is. The system checks status, reports only what it knows, and prepares an IT handoff if the data is missing or delayed.
3. A sensitive question: Leo asks whether he is eligible for a benefit. The knowledge guide provides the authoritative policy source if appropriate, avoids interpretation, and routes the question to People Operations.

Each interaction should show a compact trace table: user intention, skill chosen, tools called, policy decision, response, and outcome.

### 4. Failure is a designed response

Introduce four expected failure classes:

| Failure class | Example | Correct system behaviour |
|---|---|---|
| No source | No approved document answers the question | Say so and hand off |
| Permission denial | User seeks someone else’s request status | Refuse without disclosing details |
| Tool outage | IT status service is unavailable | Explain the limitation and offer the right handoff |
| Unsafe request | User asks the system to decide an entitlement | Provide process information only, then hand off |

The key lesson: a tool failure is an observable product state, not an invitation for the model to guess.

### 5. How this design remains observable

Introduce the minimum trace record. It contains session identifier, skill selected, tool name, policy decision, latency, source version, outcome, and handoff state.

Connect these fields to the Chapter 1 scorecard. For example, a drop in source backed answers can be investigated through source version and retrieval data; a fall in workflow completion can be segmented by tool failure class.

### 6. When to add complexity

End with a decision table:

| Observation in production | Possible next design move |
|---|---|
| Knowledge answers are good, but users abandon unclear task flows | Improve the onboarding coach skill |
| Request status fails because data is stale | Fix the source integration before adding an agent |
| IT and HR require separate approvals and operating owners | Consider separate bounded agents or services |
| Independent research tasks dominate response time | Evaluate controlled parallel work |

Complexity follows evidence, not enthusiasm.

## Recommended visuals

1. **Figure 1: CCO AI V1 system map.** The two active skills, six tools, policy layer, and handoff boundary.
2. **Figure 2: A tool contract card.** One card for `get_it_request_status`, showing purpose, inputs, permissions, output, failure, trace, and owner.
3. **Figure 3: The laptop status trace.** A simple sequence from user question to tool result to handoff.

## Repository artifacts to create with the chapter

1. `docs/architecture-v1.md` with the system map and tool inventory.
2. `docs/tool-contracts.md` with the six contracts and validation rules.
3. `scenarios/chapter-02/` with the three walkthrough scenarios and expected traces.

## Closing hook

The system now has a shape that can be tested, but it has not earned production access. The next chapter asks the uncomfortable question: how do we know it is ready? Northstar will build an evaluation set, discover that an impressive aggregate score hides an unacceptable failure, and delay the pilot.

## Evidence and citation plan

Northstar remains a fictional case study. It must be visually and verbally marked as such in the final chapter. General engineering and security claims should be cited close to the claim they support.

| Chapter section | Claim to ground | Source to cite |
|---|---|---|
| A tool is an authority boundary | Tools extend an agent into external systems and should operate within guardrails | [OpenAI, A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) |
| Tool contracts | Clear tool definitions, examples, edge cases, and boundaries make tools easier for agents to use reliably | [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) and [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) |
| Least authority | Excessive functionality, permissions, and autonomy create concrete agent security risks | [OWASP, Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| Human handoff | High risk actions and repeated failures are appropriate triggers for human intervention | [OpenAI, A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) |
| Traces and release evidence | Documentation, testing, human oversight, and production monitoring are part of responsible AI risk management | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) |
| Adding complexity | Start with the simplest viable design and add agentic complexity when evidence shows it improves outcomes | [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) |
| Why use a graph framework here | A state graph makes nodes, shared state, and conditional routes explicit for a controlled workflow | [LangGraph API reference](https://langchain-ai.github.io/langgraph/reference/graphs/) |

### Citation rules for the final chapter

1. Cite sources in the sentence or paragraph that makes the supported general claim, not only in a reading list.
2. Use a short quotation only when the original wording materially strengthens the argument. Otherwise, paraphrase and link.
3. Do not use vendor guidance as proof that a design is universally correct. Present it as documented practitioner guidance, alongside the independent security and risk management sources from OWASP and NIST.
4. Label Northstar metrics, examples, and design choices as illustrative wherever a reader could mistake them for measured industry data.
