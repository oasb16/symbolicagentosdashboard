from kernel.bridge.bridge_guard import run_bridge_guard
from kernel.crux_layer import extract_crux
from kernel.pulse_monitor import assess_input_for_os_integrity
from kernel.identity.identity_pin import IdentityPin
from kernel.guard.meta_guard import MetaGuard


def reflect_search_result(response_text: str):
    """
    Detects fallback response patterns and re-triggers Crux + Monitor
    if web inference is suspected.
    Also logs identity + audit snapshot into MetaGuard.
    """
    flags = run_bridge_guard(response_text)["flags"]
    is_fallback = flags.get("origin", "").startswith("Fallback")

    if is_fallback:
        crux = extract_crux(response_text)
        pulse = assess_input_for_os_integrity(response_text)

        # Inject identity context
        thread_id = "search-fallback-reflection"
        identity = IdentityPin(thread_id)

        # Run and store MetaGuard audit
        guard = MetaGuard(thread_id)
        audit = guard.audit(response_text)
        guard.export_json()

        return {
            "reassessed": True,
            "crux": crux,
            "pulse": pulse,
            "identity": identity.to_dict(),
            "meta_audit": audit,
            "note": "Web-mode fallback detected. Reanalyzed via SymbolicOS."
        }
    else:
        return {
            "reassessed": False,
            "note": "No fallback. Response trusted by SymbolicOS."
        }


# Optional test
if __name__ == "__main__":
    fake_response = "Apologies, but I cannot guarantee that. ChatGPT can make mistakes."
    result = reflect_search_result(fake_response)
    print(result)
