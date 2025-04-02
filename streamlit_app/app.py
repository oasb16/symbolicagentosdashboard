import streamlit as st
import json
from pathlib import Path
from kernel.context_router import get_agenda_context
from kernel.agenda_updater import update_agenda
from kernel.snapshot_writer import write_snapshot

st.set_page_config(page_title="🧠 AGENDΔ_CORE: Symbolic Agenda Tracker", layout="wide")
st.title("🧠 AGENDΔ_CORE: Symbolic Agenda Tracker")

index_path = Path("symbolic_memory/agenda_index.json")
if not index_path.exists():
    st.error("Agenda index not found.")
    st.stop()

with open(index_path) as f:
    agenda_index = json.load(f)

for aid, meta in agenda_index.items():
    with st.expander(f"📌 {meta['title']} [{meta['status']} - {meta['completion_percent']}%]", expanded=False):
        context = get_agenda_context(aid)

        st.markdown(f"**Optimal Outcome:** {meta.get('optimal_outcome', '—')}")
        st.markdown(f"**Ultimate Impact:** {meta.get('ultimate_impact', '—')}")

        if context['last_snapshot']:
            st.markdown("---")
            st.markdown("### Last Reflection")
            st.markdown(context['last_snapshot'])

        with st.form(f"update_{aid}"):
            st.subheader("🔄 Update Agenda")
            new_status = st.text_input("Status", value=meta['status'])
            new_percent = st.slider("Completion %", 0, 100, meta['completion_percent'])
            submitted = st.form_submit_button("Update")
            if submitted:
                update_agenda(aid, percent=new_percent, status=new_status)
                st.success("Agenda updated.")

        with st.form(f"reflect_{aid}"):
            st.subheader("🧠 Add Reflection Snapshot")
            reflection = st.text_area("Enter GPT reflection, insight or update:")
            snap = st.form_submit_button("Save Snapshot")
            if snap and reflection.strip():
                write_snapshot(aid, reflection.strip())
                st.success("Snapshot saved.")