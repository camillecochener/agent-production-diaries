# Article 01 — Before the Agent: Designing for Production

## Series context

**Series:** *The Agent Production Diaries*  
**Season 1:** From idea to a controlled production system  
**Case study:** *Northstar*, a fictional 8,000-person company, is considering an AI onboarding companion: the **Chief Culture Officer AI** (CCO AI).

This first article deliberately takes place *before* an agent is built. Its argument is simple: production readiness starts with the decisions that determine what success, failure, and acceptable risk mean—not with a framework, a model, or a prompt.

## Reader promise

By the end, the reader can turn a vague request—“build an onboarding agent”—into a production brief with:

- a bounded first use case;
- measurable business and operational outcomes;
- explicit non-goals and risk limits;
- an initial evaluation plan;
- a small, justified first architecture.

## Target reader and tone

- AI engineers, product managers, and technical leads moving from prototype to production.
- Practical and narrative, not framework-led.
- No claim that multi-agent architecture is automatically better.
- Estimated reading time: 8 minutes / 1,400–1,700 words.

## Narrative cast

| Person | Role in the story | What they care about |
|---|---|---|
| Maya | Head of People Operations | A calmer, more consistent first week for new hires |
| Leo | New software engineer | A laptop, access, clear next steps, and no awkward uncertainty |
| Priya | IT Operations lead | Correct access, reliable fulfilment, and no unauditable automation |
| Ana | AI product lead / narrator | Outcomes, safety boundaries, evidence for every decision |

## Opening scene (150–200 words)

Open with a Monday-morning contrast. Leo is due to start at 09:00. His welcome email is warm, but his laptop has not arrived; the shared drive is inaccessible; a calendar invitation conflicts with mandatory security training. Maya proposes an AI “Chief Culture Officer” that will make onboarding friendly, playful, and automatic.

The narrator agrees with the ambition, then reframes it:

> Before asking what the agent can do, we need to decide what it is allowed to do, how it can fail, and how we will know it helped.

Avoid showing code or a model diagram here. The tension is product ambiguity, not implementation difficulty.

## Core thesis

An agent in production is a product with delegated decisions and side effects. Therefore its design begins with an operating contract:

1. the user outcome it owns;
2. the boundaries of its authority;
3. the evidence required to release it;
4. the signals that tell the team to intervene.

## Article flow

### 1. The request is too broad (200 words)

Start from the tempting brief: “Make onboarding engaging and automate the admin.” Explain why it hides several distinct jobs:

- answering policy questions;
- giving a new hire a next best action;
- requesting or checking IT tasks;
- arranging social moments;
- running optional onboarding quests.

These do not share the same risk, permissions, reliability expectation, or definition of success. A single sentence in a product brief is not an agent specification.

### 2. Choose the first job to be done (200 words)

Define the narrow V1 promise:

> During their first five working days, a new hire can ask CCO AI what to do next and get a grounded answer, a relevant resource, or a clear handoff to a human.

V1 can read approved onboarding knowledge and create **requests** for systems of record. It cannot autonomously provision access, order equipment, make HR decisions, or publish public announcements.

This is the first deliberate trade-off: trust and learning velocity over apparent autonomy.

### 3. Write measurable success criteria (250 words)

Introduce a concise scorecard. Explain that each metric has an owner, a baseline, a release threshold, and a decision it can trigger.

| Dimension | V1 measure | Initial target | Why it exists |
|---|---|---:|---|
| Business | New hires completing the first-week checklist | +15% vs. baseline | Is onboarding actually easier? |
| Adoption | Eligible new hires active in their first week | ≥60% | Is the product useful enough to try? |
| Resolution | Sessions resolved without avoidable human follow-up | ≥70% | Does it remove friction? |
| Quality | Correct, grounded answers on the release evaluation set | ≥90% | Does it give dependable guidance? |
| Safety | High-severity policy or privacy violations | 0 | Is the system safe to expose? |
| Performance | End-to-end P95 response time | <8 seconds | Can people use it in the flow of work? |
| Cost | Median cost per resolved session | defined budget | Can its value scale? |

Clarify that targets are hypotheses in a fictional case study, not universal benchmarks. The next article will turn them into tests.

### 4. Define risk and authority before tools (250 words)

Use an authority ladder:

| Level | Example | V1 policy |
|---|---|---|
| Inform | Explain the parental-leave policy from an approved source | Allowed |
| Recommend | Suggest a next onboarding task | Allowed |
| Prepare | Draft a request for a laptop or calendar meeting | Allowed, visible to user |
| Execute | Order equipment, create accounts, send company-wide announcement | Human approval required |
| Decide | Interpret an employment entitlement or make a people decision | Never delegated |

State the product rule: **the model may suggest; a policy layer decides what may happen; a human approves consequential actions.**

Briefly call out privacy: no training on employee conversations by default, minimise profile data, retain auditable action records, and do not expose sensitive HR data in prompts or broad retrieval indexes.

### 5. Name the skills, but resist premature multi-agent design (220 words)

Define a skill as a reusable capability with instructions, allowed inputs, tools, policies, and success checks—not merely a prompt label.

The long-term system may need these skills:

- **Onboarding coach:** turn a newcomer’s situation into safe, practical next steps;
- **Knowledge guide:** search and cite approved HR/IT onboarding content;
- **IT request coordinator:** prepare, track, and escalate fulfilment requests;
- **Culture facilitator:** offer optional buddy introductions and low-pressure quests;
- **Incident triage:** recognise when the experience is blocked and hand off with context.

But V1 activates only the first two skills and one read-only request-status integration. The other skills are part of the roadmap, not an excuse to ship extra authority.

Make the multi-agent position explicit:

> We are not starting with several agents. Separate agents become useful only when teams, permissions, context, or independent workflows genuinely need separation. Until evidence says otherwise, one observable orchestrator is easier to evaluate and operate.

### 6. The first architecture is intentionally boring (180 words)

Present a small architecture diagram:

```text
New hire
  → CCO AI orchestrator
      → onboarding-coach skill
      → knowledge-guide skill → approved knowledge base
      → request-status tool (read only)
  → answer with source links, confidence signal, or human handoff
```

Mention the required production seams, without implementation detail: identity, access control, retrieval permissions, structured tool calls, tracing, feedback, and a feature flag. The agent is not trusted to define its own privileges.

### 7. Establish the release evidence (150 words)

End with a release checklist teaser:

- a representative evaluation set covering common questions, missing information, prompt injection attempts, and sensitive HR cases;
- quality and safety thresholds from the scorecard;
- test accounts and a manual escalation path;
- trace fields that capture retrieval, tool calls, latency, cost, and final outcome;
- a rollback switch.

The first article does not prove readiness. It defines what must be proven.

## Closing (100 words)

Return to Leo. CCO AI is not live yet, and that is the right outcome. The team now knows that it is not building “an HR chatbot”; it is building a narrow, traceable onboarding capability with a specific promise and a limited authority boundary.

Close with the hook for Article 2:

> Next, the team will build the first version: one agent, six tools on the roadmap, and only enough autonomy to earn trust. Before launch, it will need to pass tests that a polished demo would never reveal.

## Suggested visuals

1. **Hero visual:** “The onboarding promise vs. the production contract” — a friendly welcome flow on one side; explicit outcomes, authority, and signals on the other.
2. **Authority ladder:** Inform → Recommend → Prepare → Execute → Decide, with V1 permissions highlighted.
3. **One-page scorecard:** the success-metric table above.
4. **V1 architecture:** the deliberately small architecture diagram.

## Repository artifact for this article

Create `docs/product-brief-v1.md` next. It should contain the V1 product promise, users, non-goals, authority policy, scorecard, assumptions, and open questions. It becomes the reference against which future production decisions are assessed.

## Editorial guardrails

- Do not present gamification as a universal good; make it optional and non-competitive by default.
- Do not imply that RAG solves correctness, or that an LLM score is sufficient evidence.
- Do not claim that agentic behavior means unrestricted autonomous action.
- Avoid vendor-specific implementation details in this first post; the operating principles should outlast frameworks.
