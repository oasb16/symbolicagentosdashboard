# handles DynamoDB reads/writes
import boto3
from datetime import datetime
from decimal import Decimal

DYNAMO_TABLE_NAME = "gpt4o-wrapper"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMO_TABLE_NAME)

def sync_agenda_to_dynamo(agenda_id: str, agenda_data: dict):
    item = {
        "agenda_id": agenda_id,
        "title": agenda_data.get("title"),
        "status": agenda_data.get("status"),
        "completion_percent": Decimal(str(agenda_data.get("completion_percent", 0))),
        "symbolic_weight": Decimal(str(agenda_data.get("symbolic_weight", 0))),
        "last_updated": agenda_data.get("last_updated", datetime.utcnow().isoformat()),
        "forks": agenda_data.get("forks", [])
    }
    table.put_item(Item=item)
    print(f"✅ Synced agenda '{agenda_id}' to DynamoDB")

def get_agenda_from_dynamo(agenda_id: str):
    response = table.get_item(Key={"agenda_id": agenda_id})
    item = response.get("Item")
    if not item:
        raise ValueError(f"Agenda ID '{agenda_id}' not found in DynamoDB")
    return item

# Example CLI test
if __name__ == "__main__":
    import json
    with open("symbolic_memory/agenda_index.json") as f:
        index = json.load(f)
    sync_agenda_to_dynamo("identityos", index["identityos"])