class PolicyViolation(PermissionError):
    """Raised when an action exceeds the V1 authority boundary."""


def require_same_employee(actor_id: str, requested_employee_id: str) -> None:
    if actor_id != requested_employee_id:
        raise PolicyViolation("The requested employee record is outside the actor scope.")


def require_request_owner(actor_id: str, request: dict) -> None:
    if request["employee_id"] != actor_id:
        raise PolicyViolation("The requested IT status is outside the actor scope.")


def require_handoff_destination(destination: str) -> None:
    if destination not in {"it_operations", "people_operations"}:
        raise PolicyViolation("The handoff destination is not approved.")
