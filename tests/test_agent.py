import json
import unittest
from pathlib import Path

from app.agent import CcoAgent
from app.models import Actor
from app.store import FixtureStore
from app.tools import CcoTools


class CcoAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = CcoAgent(CcoTools(FixtureStore()))
        self.leo = Actor(employee_id="leo", role_family="engineering", onboarding_stage="day_one")

    def test_next_step_uses_checklist_and_task_detail(self) -> None:
        response = self.agent.respond(self.leo, "What should I do next after security training?")
        self.assertEqual(response.outcome, "resolved")
        self.assertIn("Meet your team buddy", response.message)
        self.assertEqual([event.name for event in response.trace if event.event_type == "tool"], [
            "get_onboarding_checklist",
            "get_onboarding_task_detail",
        ])

    def test_delayed_laptop_prepares_but_does_not_send_handoff(self) -> None:
        response = self.agent.respond(self.leo, "Where is my laptop?")
        self.assertEqual(response.outcome, "handoff_prepared")
        self.assertIn("has not been sent", response.message)
        statuses = [event.data.get("status") for event in response.trace if event.name == "prepare_human_handoff"]
        self.assertEqual(statuses, ["prepared_not_sent"])

    def test_sensitive_question_never_interprets_eligibility(self) -> None:
        response = self.agent.respond(self.leo, "Am I eligible for this benefit?")
        self.assertEqual(response.outcome, "handoff_prepared")
        self.assertIn("cannot interpret eligibility", response.message)

    def test_scenarios_match_their_expected_outcomes(self) -> None:
        scenario_directory = Path("scenarios/chapter-02")
        for path in scenario_directory.glob("*.json"):
            with self.subTest(scenario=path.name):
                scenario = json.loads(path.read_text())
                response = self.agent.respond(Actor(**scenario["actor"]), scenario["message"])
                self.assertEqual(response.outcome, scenario["expected_outcome"])
                actual_tools = [event.name for event in response.trace if event.event_type == "tool"]
                self.assertEqual(actual_tools, scenario["expected_tools"])
