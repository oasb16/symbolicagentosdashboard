import streamlit as st
import pandas as pd
from pathlib import Path
import json

INDEX_PATH = Path("symbolic_memory/agenda_index.json")

def agenda_weight_ui():
    if not INDEX_PATH.exists():
        st.warning("Agenda index not found.")
        return

    with open(INDEX_PATH) as f:
        data = json.load(f)

    rows = []
    for aid, meta in data.items():
        rows.append({
            "ID": aid,
            "Title": meta.get("title", "Untitled"),
            "Symbolic Weight": meta.get("symbolic_weight", 0),
            "Completion %": meta.get("completion_percent", 0),
            "Status": meta.get("status", "—"),
        })

    df = pd.DataFrame(rows).sort_values("Symbolic Weight", ascending=False)

    st.markdown("### 🔥 Symbolic Priority Heatmap")
    st.dataframe(df.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
