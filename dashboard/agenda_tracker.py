import streamlit as st
import openai
import pandas as pd
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache_data(show_spinner=False)
def fetch_agendas():
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are AGENDΔ_CORE, a symbolic cognition layer that tracks and prioritizes all live agendas of a Cognitive OS."},
            {"role": "user", "content": "Return the current active agendas as a JSON list. Each item must contain: title, status, completion_percent, optimal_outcome, ultimate_impact. No explanation, only raw JSON list."}
        ]
    )
    try:
        st.write(response.choices[0].message.content)
        agendas = json.loads(response.choices[0].message.content)
        return agendas
    except Exception as e:
        st.error("Failed to parse agendas: " + str(e))
        return []

def generate_agenda_ui():
    st.title("🧠 AGENDΔ_CORE: Live Agenda Tracker")

    agendas = fetch_agendas()
    if not agendas:
        st.warning("No agendas found or GPT query failed.")
        return

    df = pd.DataFrame(agendas)
    df.sort_values(by="completion_percent", ascending=False, inplace=True)
    st.dataframe(df.style.background_gradient(cmap='Blues'), use_container_width=True)
