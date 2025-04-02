import boto3
from pathlib import Path

BUCKET_NAME = "gpt4o-wrapper"
EXPORTS_DIR = Path("exports")

s3 = boto3.client("s3")

def upload_to_s3(file_path: Path, s3_key: str):
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")
    
    s3.upload_file(str(file_path), BUCKET_NAME, s3_key)
    print(f"✅ Uploaded to s3://{BUCKET_NAME}/{s3_key}")

def list_s3_seeds(prefix="cogseed_"):
    result = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    contents = result.get("Contents", [])
    return [obj["Key"] for obj in contents]

def download_from_s3(s3_key: str, local_path: Path):
    local_path.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(BUCKET_NAME, s3_key, str(local_path))
    print(f"✅ Downloaded from s3://{BUCKET_NAME}/{s3_key} to {local_path}")


# Example CLI usage
if __name__ == "__main__":
    latest = sorted(EXPORTS_DIR.glob("cogseed_*.zip"))[-1]
    upload_to_s3(latest, f"cogseeds/{latest.name}")
