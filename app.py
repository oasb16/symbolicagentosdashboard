import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import openai
import os, re

from kernel.context_router import get_agenda_context
from kernel.agenda_updater import update_agenda
from kernel.snapshot_writer import write_snapshot
from kernel.crux_layer import extract_crux
from viewer import streamlit_snapshot_viewer
from cloud_integrations.aws.s3_sync_hooks import sync_all, download_agenda
from dashboard.agenda_weight_ui import agenda_weight_ui

st.set_page_config(page_title="🧠 AGENDΔ_CORE: Symbolic Agenda Tracker", layout="wide")

# Constants
INDEX_PATH = Path("symbolic_memory/agenda_index.json")

# Load/save helpers
def load_index():
    if INDEX_PATH.exists():
        with open(INDEX_PATH) as f:
            return json.load(f)
    return {}

def save_index(index):
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

# Sync buttons
view_mode = st.sidebar.selectbox("🧭 View Mode", ["🔥 Priority Heatmap", "📊 Tracker", "📂 Snapshots"])

if st.sidebar.button("🛰 Sync to S3"):
    sync_all()
    st.sidebar.success("Symbolic memory synced to S3.")

if st.sidebar.button("🔁 Restore from S3"):
    download_agenda()
    st.success("Agenda restored from S3. Refresh to view.")

# Tracker View
if view_mode == "📊 Tracker":
    st.title("🧠 AGENDΔ_CORE: Symbolic Agenda Tracker")
    index = load_index()

    for aid, meta in index.items():
        with st.expander(f"📌 {meta['title']} [{meta['status']} - {meta['completion_percent']}%]"):
            context = get_agenda_context(aid)
            crux = extract_crux(context)

            st.markdown(f"**Symbolic Insight:** {crux['insight']}")
            if crux.get("conflict"):
                st.warning("⚠️ Conflict detected.")
            if crux.get("priority_shift"):
                st.info("🔀 Priority shift noted.")

            st.markdown(f"**Optimal Outcome:** {meta.get('optimal_outcome', '—')}")
            st.markdown(f"**Ultimate Impact:** {meta.get('ultimate_impact', '—')}")

            if context.get('last_snapshot'):
                st.markdown("### Last Reflection")
                st.markdown(context['last_snapshot'])

            with st.form(f"update_{aid}"):
                st.subheader("🔄 Update Agenda")
                new_status = st.text_input("Status", value=meta['status'])
                new_percent = st.slider("Completion %", 0, 100, meta['completion_percent'])
                submitted = st.form_submit_button("Update")
                if submitted:
                    update_agenda(aid, percent=new_percent, status=new_status, context=context)
                    st.success("Agenda updated.")

            with st.form(f"reflect_{aid}"):
                st.subheader("🧠 Add Reflection Snapshot")
                reflection = st.text_area("Enter GPT reflection, insight or update:")
                snap = st.form_submit_button("Save Snapshot")
                if snap and reflection.strip():
                    write_snapshot(aid, reflection.strip())
                    st.success("Snapshot saved.")

# Snapshot view
elif view_mode == "📂 Snapshots":
    streamlit_snapshot_viewer()

# Heatmap view
elif view_mode == "🔥 Priority Heatmap":
    agenda_weight_ui()

# ----------------------------
# Add/Edit/Delete Agenda Sidebar
# ----------------------------
def add_agenda_form():
    action = st.sidebar.selectbox("🧭 WORK ON AGENDA", ["✅ Select Action", "🔥 Add Agenda", "📊 Delete Agenda", "📂 Edit Agenda"])
    index = load_index()

    if action == "🔥 Add Agenda":
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
                index[aid] = {
                    "title": title,
                    "status": status,
                    "completion_percent": percent,
                    "symbolic_weight": symbolic_weight,
                    "last_updated": now
                }
                save_index(index)
                st.success(f"✅ Agenda '{title}' added.")

    elif action == "📊 Delete Agenda":
        st.sidebar.markdown("### 🗑️ Delete Agenda")
        if index:
            aid = st.sidebar.selectbox("Select Agenda to Delete", list(index.keys()))
            if st.sidebar.button("Delete"):
                title = index[aid]["title"]
                del index[aid]
                save_index(index)
                st.success(f"🗑️ Agenda '{title}' deleted.")
        else:
            st.sidebar.warning("⚠️ No agendas to delete.")

    elif action == "📂 Edit Agenda":
        st.sidebar.markdown("### ✏️ Edit Agenda")
        if index:
            aid = st.sidebar.selectbox("Select Agenda to Edit", list(index.keys()))
            agenda = index[aid]
            with st.sidebar.form("edit_agenda_form"):
                title = st.text_input("Agenda Title", agenda["title"])
                status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(agenda["status"]))
                percent = st.slider("Completion %", 0, 100, agenda["completion_percent"])
                symbolic_weight = st.slider("Symbolic Weight", 1, 10, agenda["symbolic_weight"])
                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    agenda.update({
                        "title": title,
                        "status": status,
                        "completion_percent": percent,
                        "symbolic_weight": symbolic_weight,
                        "last_updated": datetime.utcnow().isoformat()
                    })
                    save_index(index)
                    st.success(f"✏️ Agenda '{title}' updated.")
        else:
            st.sidebar.warning("⚠️ No agendas to edit.")

# ----------------------------
# GPT-Powered Generator
# ----------------------------
def gpt_agenda_input():
    st.sidebar.markdown("### 🤖 GPT-Powered Agenda Generator")
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    with st.sidebar.form("gpt_agenda_form"):
        idea = st.text_input("Describe symbolic initiative")
        run = st.form_submit_button("Generate via GPT")
        if run and idea:
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are AGENDΔ_CORE, a symbolic agenda architect. "
                                "Output a JSON object with: 'title', 'status', 'completion_percent', 'symbolic_weight'."
                            )
                        },
                        {"role": "user", "content": f"Generate a symbolic agenda for: {idea}"}
                    ]
                )
                raw = response.choices[0].message.content.strip()
                st.code(raw, language='json')
                raw = re.sub(r"```(?:json)?\n?", "", raw).strip("` \n")
                raw = raw.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"').strip()
                if not raw.startswith("["):
                    st.warning("⚠️ GPT returned non-JSON agenda output.")
                    return []
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

# Run Forms
add_agenda_form()
gpt_agenda_input()
