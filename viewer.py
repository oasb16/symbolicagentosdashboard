from pathlib import Path
import streamlit as st

SNAPSHOT_DIR = Path("snapshots")

def streamlit_snapshot_viewer():
    st.title("📂 Agenda Snapshots")
    if not SNAPSHOT_DIR.exists():
        st.info("No snapshots directory found.")
        return

    snapshots = sorted(SNAPSHOT_DIR.glob("*.md"))
    if not snapshots:
        st.info("No snapshot files available.")
        return

    for snap_file in snapshots:
        with st.expander(f"📄 {snap_file.stem}"):
            st.code(snap_file.read_text(), language="markdown")
