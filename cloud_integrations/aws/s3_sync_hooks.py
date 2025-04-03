import boto3
from pathlib import Path
import os

BUCKET = os.getenv("S3_BUCKET", "symbolic-agent-bucket")
REGION = os.getenv("AWS_REGION", "us-east-1")
AGENDA_FILE = Path("symbolic_memory/agenda_index.json")
SNAPSHOT_DIR = Path("snapshots")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)

def upload_agenda():
    if AGENDA_FILE.exists():
        s3.upload_file(str(AGENDA_FILE), BUCKET, f"memory/{AGENDA_FILE.name}")
        print("✅ agenda_index.json uploaded to S3.")

def upload_snapshots():
    if not SNAPSHOT_DIR.exists():
        print("⚠️ No snapshots to upload.")
        return
    for snap in SNAPSHOT_DIR.glob("*.md"):
        s3.upload_file(str(snap), BUCKET, f"snapshots/{snap.name}")
    print("✅ All snapshots uploaded to S3.")

def sync_all():
    upload_agenda()
    upload_snapshots()
