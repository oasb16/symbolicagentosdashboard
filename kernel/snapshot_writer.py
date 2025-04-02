import json
import os
from datetime import datetime
from pathlib import Path

SNAPSHOT_DIR = Path("agenda_snapshots")
LOGBOOK_PATH = Path("logs/symbolic_logbook.csv")


def load_agenda_index():
    with open("symbolic_memory/agenda_index.json", "r") as f:
        return json.load(f)


def write_snapshot(agenda_id: str, reflection: str):
    index = load_agenda_index()
    if agenda_id not in index:
        raise ValueError("Agenda not found in index")

    agenda = index[agenda_id]
    version = get_next_version(agenda_id)
    filename = SNAPSHOT_DIR / f"{agenda_id}_v{version}.md"
    timestamp = datetime.utcnow().isoformat()

    content = f"""# Snapshot: {agenda['title']} v{version}
🗓 Date: {timestamp}

## Reflection
{reflection.strip()}

## Agenda State
- Completion: {agenda['completion_percent']}%
- Symbolic Weight: {agenda['symbolic_weight']}
- Forks: {', '.join(agenda.get('forks', []))}

"""
    filename.write_text(content)
    log_snapshot_action(agenda_id, version, timestamp)
    print(f"✅ Snapshot saved: {filename}")


def get_next_version(agenda_id):
    existing = list(SNAPSHOT_DIR.glob(f"{agenda_id}_v*.md"))
    versions = [int(p.stem.split("_v")[-1]) for p in existing if "_v" in p.stem]
    return max(versions) + 1 if versions else 1


def log_snapshot_action(agenda_id, version, timestamp):
    entry = f"{timestamp},{agenda_id},v{version},snapshot_created\n"
    with open(LOGBOOK_PATH, "a") as f:
        f.write(entry)


# Example CLI test
if __name__ == "__main__":
    sample_reflection = "- GPT advised to isolate persona routing module.\n- Urgency: Moderate.\n- Next: Simulate symbolic identity bootstrap."
    write_snapshot("identityos", sample_reflection)
