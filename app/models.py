from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Actor:
    employee_id: str
    role_family: str
    onboarding_stage: str


@dataclass
class TraceEvent:
    event_type: str
    name: str
    data: dict[str, Any]


@dataclass
class AgentResponse:
    message: str
    outcome: str
    trace: list[TraceEvent] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "outcome": self.outcome,
            "trace": [asdict(event) for event in self.trace],
        }
