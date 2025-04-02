import json
from pathlib import Path
from datetime import datetime

INDEX_PATH = Path("symbolic_memory/agenda_index.json")
LOG_PATH = Path("logs/symbolic_logbook.csv")

def load_index():
    with open(INDEX_PATH, "r") as f:
        return json.load(f)

def save_index(index):
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

def update_agenda(agenda_id: str, percent: int = None, status: str = None):
    index = load_index()
    if agenda_id not in index:
        raise ValueError(f"Agenda ID '{agenda_id}' not found")

    agenda = index[agenda_id]
    changes = []

    if percent is not None:
        agenda["completion_percent"] = percent
        changes.append(f"percent={percent}")

    if status is not None:
        agenda["status"] = status
        changes.append(f"status={status}")

    agenda["last_updated"] = datetime.utcnow().isoformat()
    save_index(index)

    log_entry = f"{agenda['last_updated']},{agenda_id},update,{';'.join(changes)}\n"
    with open(LOG_PATH, "a") as log:
        log.write(log_entry)

    print(f"✅ Updated {agenda_id}: {', '.join(changes)}")

# Example CLI use
if __name__ == "__main__":
    update_agenda("identityos", percent=45, status="Persona Layer Integrated")