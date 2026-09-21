from __future__ import annotations

import json
from pathlib import Path


class FixtureStore:
    """Loads small, synthetic data sets used by the runnable examples."""

    def __init__(self, fixture_directory: Path | None = None) -> None:
        self.fixture_directory = fixture_directory or Path(__file__).resolve().parents[1] / "fixtures"
        self.tasks = self._read("onboarding_tasks.json")
        self.knowledge = self._read("approved_knowledge.json")
        self.requests = self._read("it_requests.json")

    def _read(self, name: str) -> list[dict]:
        return json.loads((self.fixture_directory / name).read_text())

    def checklist_for(self, employee_id: str) -> list[dict]:
        return [task for task in self.tasks if employee_id in task["assigned_to"]]

    def task_by_id(self, task_id: str) -> dict | None:
        return next((task for task in self.tasks if task["task_id"] == task_id), None)

    def request_by_id(self, request_id: str) -> dict | None:
        return next((request for request in self.requests if request["request_id"] == request_id), None)

    def requests_for(self, employee_id: str) -> list[dict]:
        return [request for request in self.requests if request["employee_id"] == employee_id]

    def search_knowledge(self, query: str) -> list[dict]:
        query_words = {word.strip("?.!,").lower() for word in query.split()}
        ranked = []
        for source in self.knowledge:
            source_words = set((source["title"] + " " + source["body"]).lower().split())
            score = len(query_words & source_words)
            if score:
                ranked.append({**source, "score": score})
        return sorted(ranked, key=lambda item: item["score"], reverse=True)

    def source_by_id(self, source_id: str) -> dict | None:
        return next((source for source in self.knowledge if source["source_id"] == source_id), None)
