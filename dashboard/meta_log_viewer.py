import streamlit as st
import pandas as pd
from pathlib import Path

def show_log_viewer():
    log_path = Path("logs/symbolic_logbook.csv")
    if log_path.exists():
        df = pd.read_csv(log_path, names=["Timestamp", "Agenda ID", "Action", "Details", "Crux"])
        st.markdown("### 📘 Meta Logs")
        st.dataframe(df.sort_values("Timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No symbolic logbook found.")
