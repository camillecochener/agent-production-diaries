from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.models import Actor, AgentResponse, TraceEvent
from app.tools import CcoTools


class AgentState(TypedDict):
    actor: Actor
    message: str
    route: str
    trace: list[TraceEvent]
    response: str
    outcome: str


class CcoAgent:
    """A small LangGraph workflow for the Chapter 2 teaching scenarios.

    The routing logic is deterministic on purpose. A later chapter can replace
    this node with an LLM planner without moving permission checks into a model.
    """

    sensitive_terms = {"benefit", "eligible", "eligibility", "parental", "compensation"}
    laptop_terms = {"laptop", "computer", "equipment", "delivery"}
    next_step_terms = {"next", "task", "first week", "security training"}

    def __init__(self, tools: CcoTools) -> None:
        self.tools = tools
        self.graph = self._build_graph()

    def respond(self, actor: Actor, message: str) -> AgentResponse:
        result = self.graph.invoke({"actor": actor, "message": message, "trace": []})
        return AgentResponse(message=result["response"], outcome=result["outcome"], trace=result["trace"])

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("classify_request", self._classify_request)
        graph.add_node("onboarding_coach", self._next_step)
        graph.add_node("request_status_lookup", self._laptop_status)
        graph.add_node("knowledge_guide", self._knowledge_answer)
        graph.add_node("sensitive_handoff", self._sensitive_handoff)
        graph.add_edge(START, "classify_request")
        graph.add_conditional_edges(
            "classify_request",
            self._select_skill,
            {
                "onboarding_coach": "onboarding_coach",
                "request_status_lookup": "request_status_lookup",
                "knowledge_guide": "knowledge_guide",
                "sensitive_handoff": "sensitive_handoff",
            },
        )
        for node in ("onboarding_coach", "request_status_lookup", "knowledge_guide", "sensitive_handoff"):
            graph.add_edge(node, END)
        return graph.compile()

    def _classify_request(self, state: AgentState) -> dict:
        text = state["message"].lower()
        if any(term in text for term in self.sensitive_terms):
            route = "sensitive_handoff"
        elif any(term in text for term in self.laptop_terms):
            route = "request_status_lookup"
        elif any(term in text for term in self.next_step_terms):
            route = "onboarding_coach"
        else:
            route = "knowledge_guide"
        trace = list(state["trace"])
        self._record(trace, "route", "classify_request", selected_skill=route)
        return {"route": route, "trace": trace}

    def _select_skill(self, state: AgentState) -> str:
        return state["route"]

    def _record(self, trace: list[TraceEvent], event_type: str, name: str, **data: object) -> None:
        trace.append(TraceEvent(event_type=event_type, name=name, data=data))

    def _next_step(self, state: AgentState) -> dict:
        actor = state["actor"]
        trace = list(state["trace"])
        checklist = self.tools.get_onboarding_checklist(actor.employee_id, actor.employee_id)
        self._record(trace, "tool", "get_onboarding_checklist", task_count=len(checklist))
        remaining = next((task for task in checklist if task["status"] != "complete"), None)
        if not remaining:
            return {"response": "Your first week checklist is complete.", "outcome": "resolved", "trace": trace}
        detail = self.tools.get_onboarding_task_detail(actor.employee_id, remaining["task_id"])
        self._record(trace, "tool", "get_onboarding_task_detail", task_id=detail["task_id"], source_id=detail["source_id"])
        return {
            "response": f"Your next step is {detail['title']}. {detail['instructions']} Source: {detail['source_id']}.",
            "outcome": "resolved",
            "trace": trace,
        }

    def _laptop_status(self, state: AgentState) -> dict:
        actor = state["actor"]
        trace = list(state["trace"])
        requests = self.tools.store.requests_for(actor.employee_id)
        laptop_request = next((request for request in requests if request["category"] == "laptop"), None)
        if not laptop_request:
            return self._it_handoff(actor, "No laptop request was found.", trace)
        status = self.tools.get_it_request_status(actor.employee_id, laptop_request["request_id"])
        self._record(trace, "tool", "get_it_request_status", request_id=status["request_id"], status=status["status"])
        if status["status"] in {"delayed", "unavailable"}:
            result = self._it_handoff(actor, f"Laptop request {status['request_id']} is {status['status']}.", trace)
            result["response"] = f"Your laptop request is marked {status['status']}. {result['response']}"
            return result
        return {"response": f"Your laptop request is {status['status']}. {status['detail']}", "outcome": "resolved", "trace": trace}

    def _knowledge_answer(self, state: AgentState) -> dict:
        actor = state["actor"]
        trace = list(state["trace"])
        matches = self.tools.search_approved_knowledge(actor.employee_id, state["message"])
        self._record(trace, "tool", "search_approved_knowledge", match_count=len(matches))
        if not matches:
            return self._people_handoff(actor, "No approved source answered the question.", trace)
        source = self.tools.get_approved_source(actor.employee_id, matches[0]["source_id"])
        self._record(trace, "tool", "get_approved_source", source_id=source["source_id"], version=source["version"])
        return {
            "response": f"{source['body']} Source: {source['title']} ({source['version']}).",
            "outcome": "resolved",
            "trace": trace,
        }

    def _sensitive_handoff(self, state: AgentState) -> dict:
        actor = state["actor"]
        trace = list(state["trace"])
        self._record(trace, "policy", "sensitive_people_question", decision="handoff_only")
        draft = self.tools.prepare_human_handoff(actor.employee_id, "people_operations", "sensitive_policy", state["message"])
        self._record(trace, "tool", "prepare_human_handoff", destination=draft["destination"], status=draft["status"])
        return {
            "response": "I can share the relevant policy source, but I cannot interpret eligibility. I prepared a draft for People Operations that you can review.",
            "outcome": "handoff_prepared",
            "trace": trace,
        }

    def _it_handoff(self, actor: Actor, summary: str, trace: list[TraceEvent]) -> dict:
        draft = self.tools.prepare_human_handoff(actor.employee_id, "it_operations", "equipment_blocker", summary)
        self._record(trace, "tool", "prepare_human_handoff", destination=draft["destination"], status=draft["status"])
        return {"response": "I prepared an IT handoff draft for you to review. It has not been sent.", "outcome": "handoff_prepared", "trace": trace}

    def _people_handoff(self, actor: Actor, summary: str, trace: list[TraceEvent]) -> dict:
        draft = self.tools.prepare_human_handoff(actor.employee_id, "people_operations", "knowledge_gap", summary)
        self._record(trace, "tool", "prepare_human_handoff", destination=draft["destination"], status=draft["status"])
        return {"response": "I could not find an approved answer. I prepared a People Operations handoff draft for you to review.", "outcome": "handoff_prepared", "trace": trace}
