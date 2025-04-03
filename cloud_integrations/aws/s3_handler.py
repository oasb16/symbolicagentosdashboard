import boto3
import os
from pathlib import Path

# ---- CONFIG ----
BUCKET_NAME = os.environ.get("S3_BUCKET", "symbolic-agent-bucket")
REGION_NAME = os.environ.get("AWS_REGION", "us-east-1")
AGENDA_KEY = "agenda_index.json"
AGENDA_PATH = Path("symbolic_memory/agenda_index.json")
EXPORTS_DIR = Path("exports")

s3 = boto3.client("s3", region_name=REGION_NAME)


def upload_agenda_index():
    if AGENDA_PATH.exists():
        s3.upload_file(str(AGENDA_PATH), BUCKET_NAME, AGENDA_KEY)
        print(f"✅ Uploaded agenda_index.json to s3://{BUCKET_NAME}/{AGENDA_KEY}")
    else:
        print("❌ agenda_index.json not found.")


def download_agenda_index():
    try:
        s3.download_file(BUCKET_NAME, AGENDA_KEY, str(AGENDA_PATH))
        print(f"✅ Downloaded agenda_index.json from s3://{BUCKET_NAME}/{AGENDA_KEY}")
    except Exception as e:
        print(f"⚠️ Failed to download agenda index: {e}")


def upload_latest_seed():
    latest = sorted(EXPORTS_DIR.glob("cogseed_*.zip"))[-1]
    upload_to_s3(latest, f"cogseeds/{latest.name}")


def upload_to_s3(local_path, s3_key):
    s3.upload_file(str(local_path), BUCKET_NAME, s3_key)
    print(f"✅ Uploaded {local_path} to s3://{BUCKET_NAME}/{s3_key}")


def list_s3_seeds(prefix="cogseed_"):
    result = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    contents = result.get("Contents", [])
    return [obj["Key"] for obj in contents]


# Example CLI usage
if __name__ == "__main__":
    import sys
    if "upload" in sys.argv:
        upload_agenda_index()
    elif "download" in sys.argv:
        download_agenda_index()
    elif "upload_seed" in sys.argv:
        upload_latest_seed()
    elif "list_seeds" in sys.argv:
        print("\n".join(list_s3_seeds()))