import streamlit as st
import openai
import pandas as pd
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache_data(show_spinner=False)
def fetch_agendas():
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
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
                    "content": (
                        "Return a raw JSON array of agenda objects. Each item must contain:\n"
                        "- title (string)\n- status (string)\n- completion_percent (int)\n"
                        "- optimal_outcome (string)\n- ultimate_impact (string)\n"
                        "Do NOT wrap the response in ``` or explain anything. Just output valid JSON."
                    )
                }
            ]
        )

        raw = response.choices[0].message.content.strip()

        # Clean GPT output
        if raw.startswith("```"):
            raw = raw.split("```")[1] if "```" in raw else raw
        raw = raw.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')

        agendas = json.loads(raw)
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
