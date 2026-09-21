from app.policy import PolicyViolation, require_handoff_destination, require_request_owner, require_same_employee
from app.store import FixtureStore


class CcoTools:
    def __init__(self, store: FixtureStore) -> None:
        self.store = store

    def get_onboarding_checklist(self, actor_id: str, employee_id: str) -> list[dict]:
        require_same_employee(actor_id, employee_id)
        return self.store.checklist_for(employee_id)

    def get_onboarding_task_detail(self, actor_id: str, task_id: str) -> dict:
        task = self.store.task_by_id(task_id)
        if not task or actor_id not in task["assigned_to"]:
            raise PolicyViolation("The requested task is unavailable for this user.")
        return task

    def search_approved_knowledge(self, actor_id: str, query: str) -> list[dict]:
        del actor_id
        return self.store.search_knowledge(query)

    def get_approved_source(self, actor_id: str, source_id: str) -> dict:
        del actor_id
        source = self.store.source_by_id(source_id)
        if not source:
            raise LookupError("The approved source does not exist.")
        return source

    def get_it_request_status(self, actor_id: str, request_id: str) -> dict:
        request = self.store.request_by_id(request_id)
        if not request:
            raise LookupError("The IT request does not exist.")
        require_request_owner(actor_id, request)
        return request

    def prepare_human_handoff(self, actor_id: str, destination: str, issue_class: str, summary: str) -> dict:
        require_handoff_destination(destination)
        return {
            "draft_id": f"draft-{actor_id}-{issue_class}",
            "destination": destination,
            "issue_class": issue_class,
            "summary": summary,
            "status": "prepared_not_sent",
        }
