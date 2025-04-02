from kernel.bridge.bridge_guard import run_bridge_guard
from kernel.crux_layer import extract_crux
from kernel.pulse_monitor import assess_input_for_os_integrity


def reflect_search_result(response_text: str):
    """
    Detects fallback response patterns and re-triggers Crux + Monitor
    if web inference is suspected.
    """
    flags = run_bridge_guard(response_text)["flags"]
    is_fallback = flags.get("origin", "").startswith("Fallback")

    if is_fallback:
        crux = extract_crux(response_text)
        pulse = assess_input_for_os_integrity(response_text)

        return {
            "reassessed": True,
            "crux": crux,
            "pulse": pulse,
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