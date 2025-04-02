from datetime import datetime

# 📛 Static ID Tag — User-defined
COGNITION_ID = "OMKAR ABHAY SAWANT BHOSLE"
COGNITION_ALIAS = "Munkar7Bosle"

# 🧠 Thread Integrity Tracker
class IdentityPin:
    def __init__(self, thread_id: str):
        self.thread_id = thread_id
        self.user_id = COGNITION_ID
        self.alias = COGNITION_ALIAS
        self.verified = True
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "thread_id": self.thread_id,
            "user_id": self.user_id,
            "alias": self.alias,
            "verified": self.verified,
            "timestamp": self.timestamp
        }

    def inject_into_payload(self, payload: dict) -> dict:
        payload["identity_pin"] = self.to_dict()
        return payload

# 🛡️ Validation

def is_identity_consistent(payload: dict) -> bool:
    pin = payload.get("identity_pin", {})
    return (
        pin.get("user_id") == COGNITION_ID
        and pin.get("alias") == COGNITION_ALIAS
        and pin.get("verified") is True
    )