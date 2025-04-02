import streamlit as st
import pandas as pd
import json
from pathlib import Path

def generate_agenda_ui():
    st.title("🧠 AGENDΔ_CORE: Symbolic Agenda Tracker")

    agenda_path = Path("dashboard/data/agendas.json")
    if not agenda_path.exists():
        st.error("Agenda data not found.")
        return

    with open(agenda_path, "r") as f:
        agendas = json.load(f)

    df = pd.DataFrame(agendas)
    df.sort_values(by="completion_percent", ascending=False, inplace=True)

    st.dataframe(df.style.background_gradient(cmap='Blues'), use_container_width=True)
