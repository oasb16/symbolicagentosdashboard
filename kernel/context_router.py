import json
import os
import glob
from pathlib import Path

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def list_files(directory):
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def get_agenda_context(agenda_id: str) -> dict:
    """
    Returns the enriched symbolic context for a given agenda.
    """
    index_path = Path("symbolic_memory/agenda_index.json")
    index = load_json(index_path)

    if agenda_id not in index:
        raise ValueError(f"Agenda ID '{agenda_id}' not found.")

    agenda_data = index[agenda_id]
    snapshot_files = sorted(glob.glob(f"agenda_snapshots/{agenda_id}_v*.md"))
    last_snapshot = open(snapshot_files[-1]).read() if snapshot_files else ""
    
    context = {
        "title": agenda_data.get("title"),
        "percent": agenda_data.get("completion_percent"),
        "symbolic_weight": agenda_data.get("symbolic_weight"),
        "forks": agenda_data.get("forks", []),
        "last_snapshot": last_snapshot,
        "resources": list_files(f"agenda_resources/{agenda_id}/"),
        "last_updated": agenda_data.get("last_updated")
    }

    return context

# Example CLI invocation
if __name__ == "__main__":
    import sys
    agenda_id = sys.argv[1] if len(sys.argv) > 1 else "identityos"
    context = get_agenda_context(agenda_id)
    print(json.dumps(context, indent=2))
