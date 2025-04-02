import json
from datetime import datetime, timedelta
from pathlib import Path

INDEX_PATH = Path("symbolic_memory/agenda_index.json")

FRESHNESS_HOURS = 48
ACTIVITY_DECAY_THRESHOLD = 10  # percent stagnation


def check_agenda_health():
    with open(INDEX_PATH) as f:
        index = json.load(f)

    now = datetime.utcnow()
    alerts = []

    for aid, data in index.items():
        try:
            last = datetime.fromisoformat(data["last_updated"])
        except Exception:
            alerts.append({"aid": aid, "issue": "Missing last_updated timestamp"})
            continue

        hours_old = (now - last).total_seconds() / 3600
        if hours_old > FRESHNESS_HOURS:
            alerts.append({"aid": aid, "issue": f"Stale agenda ({int(hours_old)}h old)"})

        if data.get("completion_percent") is not None:
            if int(data["completion_percent"]) in [0, 100]:
                continue  # skip edge states
            if data["completion_percent"] < ACTIVITY_DECAY_THRESHOLD:
                alerts.append({"aid": aid, "issue": f"Low progress ({data['completion_percent']}%)"})

    return alerts


# Test output
if __name__ == "__main__":
    for alert in check_agenda_health():
        print(f"⚠️  {alert['aid']}: {alert['issue']}")
