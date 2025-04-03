import json
from pathlib import Path
from datetime import datetime

from kernel.crux_layer import extract_crux
from kernel.pulse_monitor import assess_input_for_os_integrity
from kernel.identity.identity_pin import IdentityPin
from kernel.guard.meta_guard import MetaGuard

INDEX_PATH = Path("symbolic_memory/agenda_index.json")
LOG_PATH = Path("logs/symbolic_logbook.csv")
Path("logs").mkdir(exist_ok=True)  # Ensure log directory exists


def load_index():
    with open(INDEX_PATH, "r") as f:
        return json.load(f)


def save_index(index):
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)


def update_agenda(agenda_id: str, percent: int = None, status: str = None, context: dict = None):
    index = load_index()
    if agenda_id not in index:
        raise ValueError(f"Agenda ID '{agenda_id}' not found")

    agenda = index[agenda_id]
    changes = []

    if percent is not None:
        agenda["completion_percent"] = percent
        changes.append(f"percent={percent}")

    if status is not None:
        agenda["status"] = status
        changes.append(f"status={status}")

    agenda["last_updated"] = datetime.utcnow().isoformat()
    save_index(index)

    # 🧠 SymbolicOS Integration Hooks
    # 🧠 SymbolicOS Integration Hooks
    if context:
        agenda_context = context  # keep as dict
        crux = extract_crux(agenda_context)
        pulse = assess_input_for_os_integrity(agenda_context)
        
        identity = IdentityPin(agenda_id)
        guard = MetaGuard(agenda_id)
        audit = guard.audit(agenda_context)
        guard.export_json()
    else:
        print(f"[⚠️] No context passed to update_agenda() for {agenda_id}")
    
    log_entry = f"{agenda['last_updated']},{agenda_id},update,{';'.join(changes)},crux={crux['insight']}\n"
    with open(LOG_PATH, "a") as log:
        log.write(log_entry)        

    log_entry = f"{agenda['last_updated']},{agenda_id},update,{';'.join(changes)}"
    if context:
        log_entry += f",crux={crux['insight']}"

    with open(LOG_PATH, "a") as log:
        log.write(log_entry + "\n")

    print(f"✅ Updated {agenda_id}: {', '.join(changes)}")

    if context:
        print(f"🧠 Crux: {crux['insight']}")
        print(f"🔍 Pulse: {pulse}")
        print(f"📛 Identity: {identity.to_dict()['alias']}")
        print(f"🛡️ Logged to MetaGuard")
    else:
        print("⚠️ Skipped symbolic logging due to missing context.")



# Example CLI use
if __name__ == "__main__":
    update_agenda("identityos", percent=45, status="Persona Layer Integrated")