import json
from datetime import datetime, timedelta
from pathlib import Path

INDEX_PATH = Path("symbolic_memory/agenda_index.json")

FRESHNESS_HOURS = 48
ACTIVITY_DECAY_THRESHOLD = 10  # percent stagnation

def assess_input_for_os_integrity(agenda_id, index):
    return {"status": "ok", "reason": "Stub placeholder for now"}

def check_agenda_health():
    if not INDEX_PATH.exists():
        return {}

    with open(INDEX_PATH) as f:
        index = json.load(f)

    alerts = {}
    now = datetime.utcnow()

    for aid, data in index.items():
        last_str = data.get("last_updated", None)
        if not last_str:
            alerts[aid] = "⚠️ Missing timestamp"
            continue

        try:
            last = datetime.fromisoformat(last_str)
        except Exception:
            alerts[aid] = "⚠️ Invalid timestamp format"
            continue

        try:
            hours_old = (now - last).total_seconds() / 3600
            if hours_old > 72:
                alerts[aid] = f"⚠️ Agenda stale: {int(hours_old)}h old"
        except Exception as e:
            alerts[aid] = f"⚠️ Could not compute time delta: {e}"

    return alerts

# Test output
if __name__ == "__main__":
    for alert in check_agenda_health():
        print(f"⚠️  {alert['aid']}: {alert['issue']}")
