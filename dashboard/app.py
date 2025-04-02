import streamlit as st
from dashboard.agenda_tracker import generate_agenda_ui

st.set_page_config(page_title="AGENDΔ_CORE Dashboard", layout="wide")
generate_agenda_ui()
