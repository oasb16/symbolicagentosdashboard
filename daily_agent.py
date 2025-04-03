import json
from datetime import datetime
from kernel.context_router import get_agenda_context
from kernel.crux_layer import extract_crux
from kernel.pulse_monitor import assess_input_for_os_integrity
from kernel.snapshot_writer import snapshot_agenda
from kernel.seed_packager import write_cogseed
from replant_cognition import replant
from kernel.guard.meta_guard import MetaGuard
from kernel.identity.identity_pin import IdentityPin

AGENDA_PATH = "symbolic_memory/agenda_index.json"
LOG_PATH = "logs/daily_reflection.json"

def load_agenda_index():
    with open(AGENDA_PATH, "r") as f:
        return json.load(f)

def daily_reflect():
    index = load_agenda_index()
    now = datetime.utcnow().isoformat()
    reflections = []

    for aid, data in index.items():
        context = get_agenda_context(aid)

        crux = extract_crux(json.dumps(context))
        pulse = assess_input_for_os_integrity(json.dumps(context))
        identity = IdentityPin(aid).to_dict()
        guard = MetaGuard(aid)
        audit = guard.audit(json.dumps(context))
        guard.export_json()

        snapshot_agenda(aid, context)  # Versioned backup

        if pulse.get("status") == "drifting":
            replant(f"cogseeds/{aid}_seed.json")

        reflections.append({
            "agenda_id": aid,
            "timestamp": now,
            "crux": crux,
            "pulse": pulse,
            "identity": identity,
            "audit": audit
        })

    with open(LOG_PATH, "w") as f:
        json.dump(reflections, f, indent=2)

    print("✅ Daily reflection completed and saved.")

if __name__ == "__main__":
    daily_reflect()
