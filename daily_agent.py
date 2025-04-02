import json
from datetime import datetime, timedelta
from pathlib import Path
from kernel.snapshot_writer import write_snapshot
from kernel.context_router import get_agenda_context

INDEX_PATH = Path("symbolic_memory/agenda_index.json")

FRESHNESS_THRESHOLD_HOURS = 24


def load_agendas():
    with open(INDEX_PATH) as f:
        return json.load(f)


def detect_stale_agendas(index):
    now = datetime.utcnow()
    stale = []
    for aid, data in index.items():
        if not data.get("last_updated"):
            stale.append((aid, "No timestamp"))
            continue
        last = datetime.fromisoformat(data["last_updated"])
        delta = now - last
        if delta > timedelta(hours=FRESHNESS_THRESHOLD_HOURS):
            stale.append((aid, f"Stale: {delta.days}d {delta.seconds//3600}h"))
    return stale


def generate_daily_agenda():
    index = load_agendas()
    stale_agendas = detect_stale_agendas(index)
    if not stale_agendas:
        print("✅ All agendas are fresh.")
        return

    summary_lines = []
    for aid, reason in stale_agendas:
        context = get_agenda_context(aid)
        line = f"- {context['title']} ({context['percent']}%) → ⚠️ {reason}"
        summary_lines.append(line)
        write_snapshot(aid, f"Daily ping: {reason}\nNo update for {aid}. Consider reflection.")

    summary = "\n".join(summary_lines)
    print("\n📌 Daily Symbolic Alert:\n" + summary)


if __name__ == "__main__":
    generate_daily_agenda()
