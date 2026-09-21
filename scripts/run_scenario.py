import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent import CcoAgent
from app.models import Actor
from app.store import FixtureStore
from app.tools import CcoTools


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/run_scenario.py <scenario.json>")
    scenario = json.loads(Path(sys.argv[1]).read_text())
    actor = Actor(**scenario["actor"])
    agent = CcoAgent(CcoTools(FixtureStore()))
    response = agent.respond(actor, scenario["message"])
    print(json.dumps(response.to_dict(), indent=2))


if __name__ == "__main__":
    main()
