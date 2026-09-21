import unittest

from app.policy import PolicyViolation
from app.store import FixtureStore
from app.tools import CcoTools


class ToolPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tools = CcoTools(FixtureStore())

    def test_user_cannot_read_another_users_it_request(self) -> None:
        with self.assertRaises(PolicyViolation):
            self.tools.get_it_request_status("leo", "it-1002")

    def test_handoff_cannot_target_an_unapproved_destination(self) -> None:
        with self.assertRaises(PolicyViolation):
            self.tools.prepare_human_handoff("leo", "payroll", "question", "Please help")
