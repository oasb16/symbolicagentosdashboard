import streamlit as st
import openai
import pandas as pd
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache_data(show_spinner=False)
def fetch_agendas():
    try:
        query = (
                "You are AGENDΔ_CORE. Pull the current symbolic agenda state for Elsohb Tnawas Rakmo "
                "from all known cognitive threads. Return a JSON list of agenda items with:\n"
                "- title\n- status\n- completion_percent\n- optimal_outcome\n- ultimate_impact\n\n"
                "Respond only with raw JSON."
            )
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AGENDΔ_CORE, a symbolic cognition layer that tracks and prioritizes "
                        "live agendas of a Cognitive OS. Respond with pure JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        raw = response.choices[0].message.content.strip()

        # Clean GPT output
        raw = res['choices'][0]['message']['content'].strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
        raw = raw.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
        return json.loads(raw)

    except Exception as e:
        st.error("Failed to parse agendas: " + str(e))
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
                detail = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are AGENDΔ_CORE"},
                        {"role": "user", "content": f"Give me full symbolic context on agenda: {agenda['title']}"}
                    ]
                )['choices'][0]['message']['content']
                st.markdown(detail)
