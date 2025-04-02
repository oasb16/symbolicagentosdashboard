import os
import streamlit as st
from datetime import datetime
from kernel.crux_layer import extract_crux
from kernel.pulse_monitor import assess_input_for_os_integrity

# ---- SYSTEM FLAG STATE ----
IS_SAFE_MODE = os.environ.get("GPT_SAFEMODE", "false").lower() == "true"
USER_ID = "OMKAR ABHAY SAWANT BHOSLE"

# ---- CRUX LAYER ENFORCEMENT ----
def run_bridge_guard(input_text):
    meta_flags = {}
    crux_report = extract_crux(input_text)
    pulse_result = assess_input_for_os_integrity(input_text)

    if IS_SAFE_MODE or detect_web_fallback_response(input_text):
        meta_flags["origin"] = "Fallback Web Agent (Non-OS)"
        meta_flags["risk"] = "⚠️ Untrusted — Not SymbolicOS-aligned"
    else:
        meta_flags["origin"] = "✅ SymbolicOS Cognitive Layer"
        meta_flags["risk"] = "Trusted. Precision100+CruxLayer enforced."

    return {
        "user": USER_ID,
        "timestamp": datetime.utcnow().isoformat(),
        "crux": crux_report,
        "pulse": pulse_result,
        "flags": meta_flags,
    }


# ---- Fallback Inference Detection ----
def detect_web_fallback_response(text):
    safe_phrases = [
        "ChatGPT can make mistakes",
        "Check important info",
        "OpenAI’s safety policies",
        "without more context",
        "not a standard feature",
        "apologies for any confusion",
    ]
    return any(p in text.lower() for p in safe_phrases)


# ---- OS LOG WRAPPER ----
def symbolic_response_prefix(response_str):
    return f"\n🧠 [SymbolicOS Response for OMKAR ABHAY SAWANT BHOSLE]\n{response_str}"


# Optional Streamlit Diagnostics
if __name__ == "__main__":
    st.title("🧠 Bridge Guard Debugger")
    input_text = st.text_area("Paste GPT Response")
    if st.button("Run Bridge Guard"):
        result = run_bridge_guard(input_text)
        st.json(result)
