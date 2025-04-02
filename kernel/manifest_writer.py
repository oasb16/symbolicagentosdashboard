import json
from datetime import datetime
from pathlib import Path

MANIFEST_PATH = Path("symbolic_memory/system_manifest.json")
INDEX_PATH = Path("symbolic_memory/agenda_index.json")
SNAPSHOT_DIR = Path("agenda_snapshots")
RESOURCES_DIR = Path("agenda_resources")


def generate_manifest():
    with open(INDEX_PATH, "r") as f:
        index = json.load(f)

    manifest = {
        "generated_at": datetime.utcnow().isoformat(),
        "agenda_count": len(index),
        "agendas": {}
    }

    for aid, data in index.items():
        snapshots = list(SNAPSHOT_DIR.glob(f"{aid}_v*.md"))
        resources = list((RESOURCES_DIR / aid).glob("*")) if (RESOURCES_DIR / aid).exists() else []

        manifest["agendas"][aid] = {
            "title": data["title"],
            "status": data["status"],
            "percent": data["completion_percent"],
            "symbolic_weight": data["symbolic_weight"],
            "last_updated": data["last_updated"],
            "snapshots": [s.name for s in snapshots],
            "resources": [r.name for r in resources]
        }

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Manifest generated: {MANIFEST_PATH}")


if __name__ == "__main__":
    generate_manifest()
