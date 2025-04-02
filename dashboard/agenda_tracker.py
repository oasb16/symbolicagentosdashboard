import streamlit as st
import openai
import json
import re

def load_symbolic_agendas():
    with open("symbolic_memory/agenda_store.json", "r") as f:
        return json.load(f)

@st.cache_data(ttl=3600)
def fetch_agendas():
    SYSTEM_KEY = "ΔAGENDΔ_CORE_THREAD:Elsohb_Tnawas_Rakmo"
    agendas = load_symbolic_agendas()
    anchor_titles = [f"- {a['title']}" for a in agendas]
    anchor_list = "\n".join(anchor_titles)

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AGENDΔ_CORE, a symbolic cognition OS for Elsohb Tnawas Rakmo.\n"
                        "You maintain symbolic agendas in a persistent lattice.\n"
                        "Use only the real agendas provided below as anchors. Avoid fabrication."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Here are the current symbolic agenda anchors:\n{anchor_list}\n\n"
                        "Return only valid JSON array with: title, status, completion_percent, "
                        "optimal_outcome, ultimate_impact.\n"
                        "Do not wrap in markdown or add any commentary."
                    )
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        st.code(raw, language='json')

        raw = re.sub(r"```(?:json)?\n?", "", raw).strip("` \n")
        raw = raw.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"').strip()

        if not raw.startswith("["):
            st.warning("⚠️ GPT returned non-JSON agenda output.")
            return []

        agendas = json.loads(raw)
        return agendas

    except Exception as e:
        st.error(f"❌ Failed to parse agendas: {e}")
        return []

def generate_agenda_ui():
    st.title("🧠 AGENDΔ_CORE: Symbolic Agenda Tracker")

    agendas = fetch_agendas()
    if not agendas:
        st.warning("No agendas loaded.")
        return

    for agenda in agendas:
        with st.expander(f"📌 {agenda['title']} [{agenda['status']} - {agenda['completion_percent']}%]"):
            st.markdown(f"**Optimal Outcome:** {agenda['optimal_outcome']}")
            st.markdown(f"**Ultimate Impact:** {agenda['ultimate_impact']}")
