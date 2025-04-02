import json
from datetime import datetime
from kernel.bridge.bridge_guard import run_bridge_guard
from kernel.identity.identity_pin import IdentityPin
from kernel.crux_layer import extract_crux
from kernel.pulse_monitor import assess_input_for_os_integrity


class MetaGuard:
    def __init__(self, thread_id):
        self.thread_id = thread_id
        self.identity = IdentityPin(thread_id)
        self.snapshots = []

    def audit(self, response: str):
        bridge = run_bridge_guard(response)
        crux = extract_crux(response)
        pulse = assess_input_for_os_integrity(response)

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "origin": bridge["flags"].get("origin"),
            "risk": bridge["flags"].get("risk"),
            "crux": crux,
            "pulse": pulse,
            "identity": self.identity.to_dict()
        }
        self.snapshots.append(record)
        return record

    def export_json(self, path="logs/meta_guard_snapshots.json"):
        with open(path, "w") as f:
            json.dump(self.snapshots, f, indent=2)


# Optional CLI usage
if __name__ == "__main__":
    guard = MetaGuard("test-thread")
    test_input = "ChatGPT can make mistakes."
    audit = guard.audit(test_input)
    print(json.dumps(audit, indent=2))