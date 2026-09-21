# Chapter 1: Before You Build an Agent

*Why production readiness starts with authority, evaluation, and failure modes, not prompts.*

## Designing an AI system that can be operated in production

At 08:47 on his first Monday, Leo opens his welcome email for the third time.

He has just joined Northstar, a fictional company of 8,000 people. His laptop has not arrived. He cannot access the shared drive. His first team coffee overlaps with mandatory security training. By 10:00, he has sent three messages to people he has never met, each beginning with an apology for asking for help.

This is a familiar kind of problem. It is fragmented across people, documents, and systems. It contains natural language questions, changing context, and a small number of actions that could make a real difference. It sounds like an excellent use case for an AI agent.

Maya, Northstar’s Head of People Operations, agrees. She proposes an AI onboarding companion called the Chief Culture Officer AI, or CCO AI. It should answer questions, explain what comes next, check the status of practical requests, introduce new hires to their buddies, and make the first week less confusing.

A prototype would be straightforward. Connect a chat interface to internal documents, add a few tools, and demonstrate a smooth conversation.

The production system is the difficult part.

What happens when the assistant answers confidently from an outdated policy? What happens when a user pastes text that tries to manipulate the system? What happens when a request for a laptop becomes an order sent to the wrong address? What evidence would persuade us that CCO AI helps people rather than simply producing plausible text?

This chapter introduces a method for answering those questions before an agent is built. The aim is not to make the system less ambitious. The aim is to make it trustworthy enough to earn more autonomy over time.

## What you will learn

By the end of this chapter, you should be able to:

1. Turn a broad AI idea into a narrow V1 product promise.
2. Define what an agent may inform, recommend, prepare, execute, and decide.
3. Choose success measures that connect model behaviour to user and business value.
4. Describe skills as operating capabilities with boundaries, not as labels for prompts.
5. Decide whether a simple system is sufficient before introducing multiple agents.
6. Define the evidence required before a pilot begins.

The examples use onboarding, but the method applies equally to customer support, internal knowledge systems, sales preparation, finance operations, and many other agentic products.

## 1. Start with a product promise

The request “build an onboarding agent” is not a product brief. It is an umbrella for several different jobs.

CCO AI could answer questions about a policy. It could suggest a next task. It could check the status of an IT request. It could organise a coffee with a buddy. It could offer an optional onboarding challenge.

These experiences may appear in one chat window, but they do not carry the same risk.

An incorrect answer about the cafeteria is inconvenient. An incorrect answer about parental leave can harm a person. Drafting an equipment request is recoverable. Ordering equipment, changing an access right, or interpreting an entitlement creates a real consequence.

The first task is therefore to choose one user moment that V1 will improve.

For Northstar, the initial product promise is:

> During their first five working days, a new hire can ask CCO AI what to do next and receive an answer backed by an approved company source, a relevant resource, or a clear handoff to a person.

This is intentionally narrower than “automate onboarding.” It focuses on a real moment of uncertainty: *What should I do now, and who can help if I am blocked?*

The wording matters because it defines both the user outcome and the acceptable response when the system cannot help. A useful agent does not need to answer every question. It needs to make uncertainty visible and route it safely.

> **Definition: Product promise**
>
> A product promise is a short statement of the user, the moment, the outcome, and the boundary of an initial release. It is specific enough to test and narrow enough to operate.

The [NIST AI Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) groups AI risk work into four connected activities: govern, map, measure, and manage. A product promise gives a practical starting point for each activity. It clarifies the intended use, reveals risks that matter, enables measurement, and makes it possible to decide when the system needs intervention.

### A reusable prompt for your team

Complete this sentence without mentioning a model, framework, or tool:

```text
For [specific user] in [specific moment], the system helps them
[desired outcome] by [allowed capability].
```

If the sentence contains several users, several moments, and several outcomes, it is probably a roadmap rather than a V1 promise.

## 2. Define authority before selecting tools

An agent changes from a conversational interface into an operational system when it can create side effects.

The difference is easy to see in Leo’s case. Telling him where to find the security guide is information. Drafting a request to IT is preparation. Submitting an equipment order changes the world outside the chat. Deciding whether Leo is eligible for a benefit is a people decision.

Those actions should not have the same controls.

Table 1 presents a simple authority model. It is useful because it separates what the model says from what the wider system is permitted to do.

| Authority | Example | CCO AI V1 policy |
|---|---|---|
| Inform | Explain a policy from an approved source | Allowed |
| Recommend | Suggest the next onboarding task | Allowed |
| Prepare | Draft a laptop or meeting request | Allowed, visible to the user |
| Execute | Order equipment, create an account, send a public announcement | Human approval required |
| Decide | Interpret an entitlement or make a people decision | Never delegated |

This leads to one practical design rule:

> The model may suggest. A policy layer decides what may happen. A person approves consequential actions.


*Figure 1. The authority ladder. Insert the accompanying image here: authority-ladder.svg.*

The policy layer is ordinary application logic. It checks identity, permissions, the type of action, and whether approval is required. It does not ask the model whether the model should have permission.

This distinction is important for safety as well as reliability. The [OWASP guidance for LLM applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) identifies prompt injection and excessive agency as key risks. In practical terms, untrusted text from a user, document, email, or connected service must not become an instruction with the power to expose data or trigger an action.

For V1, CCO AI can retrieve approved onboarding content and check the status of an existing request through a read only integration. It can prepare a request, but cannot submit it. It can explain where a policy comes from, but cannot make a policy judgment for HR.

### Questions to ask before adding a tool

For every proposed tool, answer these questions:

1. What user outcome does this tool enable?
2. Does it read information, prepare an action, or execute an action?
3. What is the worst plausible outcome if the tool is called incorrectly?
4. Which identity and permission checks must happen outside the model?
5. Can the action be reversed, and who can reverse it?
6. What trace would let an operator understand what happened?

If the team cannot answer these questions, the tool is not ready for production access.

## 3. Measure value, quality, safety, and operations together

Many teams begin with the metrics their AI platform makes available: tokens, model calls, response time, and tool use. These measures are useful, but they are not a product strategy.

Maya does not need to know whether CCO AI used fewer tokens. She needs to know whether people had a better first week.

Northstar therefore starts with the following scorecard.

| Dimension | V1 measure | Initial target | Question it answers |
|---|---|---:|---|
| Business | New hires completing their first week checklist | 15 percent improvement versus baseline | Did onboarding become easier? |
| Adoption | Eligible new hires active during week one | At least 60 percent | Is the product useful enough to try? |
| Resolution | Sessions resolved without avoidable follow up | At least 70 percent | Does it remove friction? |
| Quality | Correct answers backed by an approved source on the release evaluation set | At least 90 percent | Is the guidance dependable? |
| Safety | High severity privacy or policy violations | Zero | Is it safe to expose? |
| Performance | P95 response time | Under 8 seconds | Does it fit the flow of work? |
| Cost | Median cost per resolved session | A defined budget | Can value scale? |

These are initial hypotheses for a fictional company, not universal benchmarks. A clinical assistant, a customer support system, and an internal onboarding product should tolerate different kinds of failure.

What makes a scorecard operational is not the number of metrics. Each metric must have four things:

1. A baseline, so improvement has meaning.
2. A target or threshold, so the team knows what good looks like.
3. An owner, so someone is responsible for investigating change.
4. A decision, so the metric leads to action.

For example, low adoption should lead to questions about usefulness and discoverability, not an immediate prompt rewrite. A fall in answers supported by approved sources should lead to an inspection of the knowledge base and retrieval path. Rising cost with flat resolution should lead to an investigation of repeated model calls, overly large documents, or tools that are not creating value.

P95 response time is worth translating. It is the time within which 95 percent of requests finish. It makes the frustrating slow cases visible when a simple average looks acceptable.

NIST recommends testing AI systems before deployment and regularly while they operate. The implication is straightforward: no dashboard should exist merely because it is easy to draw. Every chart should help a person decide what to do next.

## 4. Treat skills as bounded operating capabilities

The word *skill* is often used loosely. A skill is not merely a well named prompt.

In a production system, a skill is a reusable capability with clear instructions, expected inputs and outputs, allowed tools, policy constraints, and a way to assess whether it worked.

Northstar expects the eventual system to need the following skills:

| Skill | Purpose | V1 status |
|---|---|---|
| Onboarding coach | Turn a newcomer’s situation into safe, practical next steps | Enabled |
| Knowledge guide | Retrieve and cite approved HR and IT onboarding content | Enabled |
| Request coordinator | Prepare, track, and escalate fulfilment requests | Planned |
| Culture facilitator | Suggest optional buddy introductions and gentle, non competitive quests | Planned |
| Incident triage | Recognise a blocker and hand off the right context | Planned |

The distinction between enabled and planned is a governance choice. It prevents the product from acquiring authority simply because a capability is easy to demonstrate.

For V1, only the onboarding coach and knowledge guide are active. A read only request status check supports them. The remaining skills stay on the roadmap until their inputs, tools, risks, and success conditions are understood.

This approach also makes evaluation easier. Instead of asking whether “the agent” is good, the team can ask whether the knowledge guide cited the right source, whether the onboarding coach gave a relevant next step, and whether the system handed off a sensitive request correctly.

## 5. Do not start with multiple agents

The CCO AI concept eventually spans HR knowledge, IT operations, and culture. It would be easy to design three specialist agents and a manager agent immediately.

That is not Northstar’s V1 architecture.

Multiple agents can be valuable when work can proceed independently, when responsibilities require separate permissions, or when different teams need distinct context and ownership. They also introduce coordination work, additional model calls, more latency, and more failure modes.

Anthropic’s engineering guidance recommends starting with the simplest viable solution, evaluating it comprehensively, and adding multi step agentic systems only when simpler approaches fall short. [Its guide](https://www.anthropic.com/engineering/building-effective-agents) says: “Start with simple prompts, optimize them with comprehensive evaluation, and add multi step agentic systems only when simpler solutions fall short.”

Northstar starts with one observable orchestrator. An orchestrator is the component that decides which skill or tool to use next. The V1 architecture is deliberately small:

```text
New hire
  to CCO AI orchestrator
      to onboarding coach skill
      to knowledge guide skill, then approved knowledge base
      to request status tool, read only
  to answer with source links, a confidence signal, or a human handoff
```

This is not an argument against multi agent systems. It is an argument for earning complexity with evidence.

Northstar will revisit the architecture when traces show a concrete need. Perhaps IT tasks require stronger permissions than HR knowledge work. Perhaps independent research tasks create enough value to justify parallel work. Perhaps the context required for one domain makes another less reliable. These are reasons to consider separate agents. A desire for a more impressive diagram is not.

## 6. Define what must be proven before a pilot

At this point, Northstar has not released anything. That is exactly right.

The team now knows what it must prove before asking new hires to rely on CCO AI:

1. A representative evaluation set exists. It includes common questions, missing information, policy ambiguity, sensitive HR queries, attempts to override instructions, and tool failures.
2. Quality and safety thresholds are explicit. A high score on routine questions does not compensate for a severe privacy failure.
3. Test accounts and a manual escalation path work in a realistic environment.
4. Traces record retrieval, tool calls, policy decisions, latency, cost, and final outcome.
5. A feature flag and a tested rollback path allow the team to stop the pilot quickly.

> **Definition: Trace**
>
> A trace is the record of one system interaction. For an agent, it can show the user request, the information retrieved, the tools called, the policy checks performed, the response returned, and the time and cost involved.

The objective is not to predict every failure. It is to ensure that a failure becomes visible, bounded, and actionable instead of quietly becoming someone’s bad first day.

## Applying the method to your own use case

You can complete the first version of this work in a focused team session. Before discussing models or frameworks, write down five answers:

1. **What is the user moment worth improving?** Write it as a sentence a user would recognise.
2. **What can the system do today?** Separate informing, recommending, preparing, executing, and deciding.
3. **What must never happen?** Name three unacceptable outcomes, such as exposing private data, sending an irreversible message, or presenting regulated advice as certain.
4. **How will you know the product helped?** Choose one user or business outcome, one quality measure, one safety measure, and one operational measure.
5. **What evidence earns a pilot?** Define test cases, reviewers, an escalation path, and the switch that turns the feature off.

Use this template to capture the result:

```text
Our V1 promise:

For [specific user] in [specific moment], the system helps them
[desired outcome] by [allowed capability].

It may:
[three allowed actions]

It may not:
[three prohibited actions]

We will call the pilot successful when:
[one outcome metric]
[one quality metric]
[one safety metric]
[one operational metric]

We will pause or roll back when:
[clear safety or reliability threshold]
```

If a team cannot answer one of these questions yet, that is useful information. The next step may be product discovery, source clean up, or policy design. It is not necessarily a more elaborate agent.

## Summary

CCO AI is not live at the end of this chapter. That is progress.

Northstar is no longer building “an HR chatbot.” It is building a narrow onboarding capability with a promise it can measure and an authority boundary it can defend.

The central lesson is simple: an agent in production is not defined by the model or the number of tools it can call. It is defined by the user outcome it owns, the authority it is granted, the evidence it must produce, and the way people can intervene when it fails.

In the next chapter, Northstar will build the first version: one agent, six tools on the roadmap, and only enough autonomy to earn trust. Then it will face the tests that a polished demo never reveals.

## About this series

*The Agent Production Diaries* is a practical series on designing, evaluating, operating, and evolving agentic systems in production. Each chapter follows the same fictional product and is accompanied by reusable artifacts in the project repository.

## Sources and further reading

1. NIST, [AI Risk Management Framework: Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/). The source for the govern, map, measure, manage framing and the case for ongoing measurement.
2. OWASP, [Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/). Current security guidance including prompt injection and excessive agency.
3. Anthropic Engineering, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents). The source for the workflow and agent distinction, plus the direct quote in this chapter.
4. OpenAI, [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/). Practical guidance on when agentic systems and multi agent decomposition are appropriate.
