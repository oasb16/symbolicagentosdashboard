import streamlit as st
import openai
import pandas as pd
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache_data(ttl=3600, show_spinner=True)
def fetch_agendas():
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are AGENDΔ_CORE, a symbolic cognition layer that tracks user agendas. Output only raw JSON."
                },
                {
                    "role": "user",
                    "content": (
                        "You are AGENDΔ_CORE.\n"
                        "Access the symbolic memory for the architect known as Elsohb Tnawas Rakmo.\n"
                        "List only the current top-level symbolic agendas they are actively tracking in the Cognitive OS, based on past architecture threads, agenda mapping, and Meta-Lattice priority.\n"
                        "Respond with pure JSON containing:\n"
                        "- title\n- status\n- completion_percent\n- optimal_outcome\n- ultimate_impact\n"
                        "No marketing fluff, no sample corporate agendas, no filler."
                    )
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        # st.code(raw, language='json')  # 🔍 For live debug visibility

        # 🧼 Sanitize possible markdown wrappers and smart quotes
        if raw.startswith("```"):
            raw = raw.split("```")[1].strip()

        raw = (
            raw.replace("‘", "'").replace("’", "'")
                .replace("“", '"').replace("”", '"')
                .strip()
        )

        agendas = json.loads(raw)
        return agendas

    except Exception as e:
        st.error(f"❌ Failed to parse agendas: {e}")
        return []


def generate_agenda_ui():
    st.title("🧠 AGENDΔ_CORE: Live Agenda Tracker")

    agendas = fetch_agendas()
    if not agendas:
        st.warning("No agendas found.")
        return

    for agenda in agendas:
        with st.expander(f"📌 {agenda['title']} [{agenda['status']} - {agenda['completion_percent']}%]"):
            st.markdown(f"**Optimal Outcome**: {agenda['optimal_outcome']}")
            st.markdown(f"**Ultimate Impact**: {agenda['ultimate_impact']}")

            # Optional GPT detail fetch
            if st.button(f"🔍 More on '{agenda['title']}'", key=agenda['title']):
                detail = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are AGENDΔ_CORE"},
                        {"role": "user", "content": f"Give me full symbolic context on agenda: {agenda['title']}"}
                    ]
                )
                detail_respo = detail.choices[0].message.content.strip()
                st.markdown(detail_respo)
