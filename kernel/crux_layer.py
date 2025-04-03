from pathlib import Path
import json
from difflib import unified_diff

SNAPSHOT_DIR = Path("agenda_snapshots")

from kernel.pulse_monitor import check_agenda_health

alerts = check_agenda_health()
for aid, issue in alerts.items():
    print(f"⚠️ {aid}: {issue}")


def extract_crux(agenda_id):
    snaps = sorted(SNAPSHOT_DIR.glob(f"{agenda_id}_v*.md"))
    if len(snaps) < 2:
        return {"insight": "Not enough history", "conflict": None, "priority_shift": None}

    with open(snaps[-2]) as f:
        prev = f.readlines()
    with open(snaps[-1]) as f:
        latest = f.readlines()

    diff = list(unified_diff(prev, latest))
    insight_lines = [line for line in diff if line.startswith("+ ") or line.startswith("- ")]
    insight = "\n".join(insight_lines[:10]) if insight_lines else "Minor or no symbolic shift"

    # Simulate symbolic detection (can be replaced with GPT or pattern detection)
    priority_shift = any("priority" in line.lower() for line in insight_lines)
    conflict = any("vs" in line.lower() or "contradiction" in line.lower() for line in insight_lines)

    return {
        "insight": insight.strip(),
        "conflict": conflict,
        "priority_shift": priority_shift,
    }


# Example CLI test
if __name__ == "__main__":
    from sys import argv
    print(json.dumps(extract_crux(argv[1]), indent=2))
