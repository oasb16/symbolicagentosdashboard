import zipfile
from pathlib import Path
import sys

SEED_DIR = Path("exports")
TARGET_ROOT = Path(".")

def replant(seed_path: Path):
    if not seed_path.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_path}")

    with zipfile.ZipFile(seed_path, 'r') as zipf:
        zipf.extractall(TARGET_ROOT)
    print(f"🌱 Cognition replanted from: {seed_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        latest = sorted(SEED_DIR.glob("cogseed_*.zip"))[-1]
        replant(latest)
    else:
        seed_path = Path(sys.argv[1])
        replant(seed_path)
