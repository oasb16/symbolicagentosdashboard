import streamlit as st
import json
from pathlib import Path
from kernel.context_router import get_agenda_context
from kernel.agenda_updater import update_agenda
from kernel.snapshot_writer import write_snapshot
from kernel.crux_layer import extract_crux
from viewer import streamlit_snapshot_viewer
from cloud_integrations.aws.s3_sync_hooks import sync_all
import uuid
from datetime import datetime
import openai
import os

st.set_page_config(page_title="🧠 AGENDΔ_CORE: Symbolic Agenda Tracker", layout="wide")


view_mode = st.sidebar.selectbox("🧭 View Mode", ["📊 Tracker", "📂 Snapshots", "🔥 Priority Heatmap"])

st.sidebar.button("🛰 Sync to S3")

if st.sidebar.button("🛰 Sync to S3"):
    sync_all()
    st.sidebar.success("Symbolic memory synced to S3.")

if view_mode == "📊 Tracker":
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

            crux = extract_crux(aid)
            st.markdown(f"**Symbolic Insight:** {crux['insight']}")
            if crux['conflict']:
                st.warning("⚠️ Conflict detected.")
            if crux['priority_shift']:
                st.info("🔀 Priority shift noted.")

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

elif view_mode == "📂 Snapshots":
    streamlit_snapshot_viewer()

elif view_mode == "🔥 Priority Heatmap":
    from dashboard.agenda_weight_ui import agenda_weight_ui
    agenda_weight_ui()

# ----------------------------
# Add Agenda Sidebar Form
# ----------------------------
def load_index():
    if index_path.exists():
        with open(index_path) as f:
            return json.load(f)
    return {}

def save_index(index):
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)

def add_agenda_form():
    st.sidebar.markdown("### ➕ Add New Agenda")
    with st.sidebar.form("new_agenda_form"):
        title = st.text_input("Agenda Title")
        status = st.selectbox("Initial Status", ["Not Started", "In Progress", "Completed"])
        percent = st.slider("Completion %", 0, 100, 0)
        symbolic_weight = st.slider("Symbolic Weight", 1, 10, 5)

        submitted = st.form_submit_button("Add Agenda")
        if submitted and title:
            aid = str(uuid.uuid4())[:8]
            now = datetime.utcnow().isoformat()
            index = load_index()
            index[aid] = {
                "title": title,
                "status": status,
                "completion_percent": percent,
                "symbolic_weight": symbolic_weight,
                "last_updated": now
            }
            save_index(index)
            st.success(f"✅ Agenda '{title}' added.")

def gpt_agenda_input():
    st.sidebar.markdown("### 🤖 GPT-Powered Agenda Generator")
    openai.api_key = os.getenv("OPENAI_API_KEY", "")  # use env key

    with st.sidebar.form("gpt_agenda_form"):
        idea = st.text_input("Describe symbolic initiative")
        run = st.form_submit_button("Generate via GPT")

        if run and idea:
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are AGENDΔ_CORE, a symbolic agenda architect."},
                        {"role": "user", "content": f"Generate a JSON agenda object for: {idea}"}
                    ]
                )
                raw = response.choices[0].message.content.strip()
                st.code(raw, language="json")

                parsed = json.loads(raw)
                aid = str(uuid.uuid4())[:8]
                now = datetime.utcnow().isoformat()
                index = load_index()
                index[aid] = parsed
                index[aid]["last_updated"] = now
                save_index(index)
                st.success(f"✅ Agenda '{parsed.get('title', 'Generated')}' added.")

            except Exception as e:
                st.error(f"GPT failed: {e}")

add_agenda_form()
gpt_agenda_input()
