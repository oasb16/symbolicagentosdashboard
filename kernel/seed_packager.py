import zipfile
from datetime import datetime
from pathlib import Path

EXPORTS_DIR = Path("exports")
SEED_NAME = f"cogseed_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
SEED_PATH = EXPORTS_DIR / SEED_NAME

INCLUDE_DIRS = [
    "symbolic_memory",
    "agenda_snapshots",
    "agenda_resources",
    "logs"
]

EXPORTS_DIR.mkdir(exist_ok=True)

def package_seed():
    with zipfile.ZipFile(SEED_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in INCLUDE_DIRS:
            path = Path(folder)
            for file in path.rglob("*"):
                if file.is_file():
                    arcname = file.relative_to(Path("."))
                    zipf.write(file, arcname)

    print(f"✅ Seed packaged: {SEED_PATH}")


if __name__ == "__main__":
    package_seed()