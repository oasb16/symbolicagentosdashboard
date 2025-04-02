import streamlit as st
import openai
import pandas as pd
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

import re

@st.cache_data(ttl=3600, show_spinner=True)
def fetch_agendas():
    SYSTEM_KEY = "ΔAGENDΔ_CORE_THREAD:Elsohb_Tnawas_Rakmo"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AGENDΔ_CORE, the symbolic cognition architecture agent.\n"
                        f"Authorized user: Elsohb Tnawas Rakmo. Identity handshake: [{SYSTEM_KEY}].\n"
                        "You persist across threads and remember all symbolic agendas defined by this user.\n"
                        "Never fabricate. Return only the real symbolic agendas from their Cognitive OS."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"AGENDΔ_CORE: pull the active symbolic agenda lattice for Elsohb Tnawas Rakmo [{SYSTEM_KEY}].\n"
                        "Return a valid JSON array with:\n"
                        "- title (string)\n- status (string)\n- completion_percent (int)\n"
                        "- optimal_outcome (string)\n- ultimate_impact (string)\n"
                        "Do NOT wrap in markdown (```json). Return raw JSON only."
                    )
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        st.code(raw, language='json')  # Debug visibility

        # 🚫 Remove all code block fences like ```json ... ```
        raw = re.sub(r"```(?:json)?\n?", "", raw).strip("` \n")

        # 🧼 Normalize quote characters
        raw = (
            raw.replace("‘", "'")
                .replace("’", "'")
                .replace("“", '"')
                .replace("”", '"')
                .strip()
        )

        if not raw.startswith("["):
            st.warning("⚠️ GPT returned content that does not begin with a JSON array.")
            return []

        agendas = json.loads(raw)
        return agendas

    except Exception as e:
        st.error(f"❌ Failed to parse agendas: {e}")
        return []


    except Exception as e:
        st.error(f"❌ Failed to parse agendas: {e}")
        return []



def generate_agenda_ui():
    st.title("🧠 AGENDΔ_CORE: Live Agenda Tracker")

    agendas = fetch_agendas()
    if not agendas:
        st.warning("No agendas found.")
        return

    for agenda in agendas:
        with st.expander(f"📌 {agenda['title']} [{agenda['status']} - {agenda['completion_percent']}%]"):
            st.markdown(f"**Optimal Outcome**: {agenda['optimal_outcome']}")
            st.markdown(f"**Ultimate Impact**: {agenda['ultimate_impact']}")

            # Optional GPT detail fetch
            if st.button(f"🔍 More on '{agenda['title']}'", key=agenda['title']):
                detail = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are AGENDΔ_CORE"},
                        {"role": "user", "content": f"Give me full symbolic context on agenda: {agenda['title']}"}
                    ]
                )
                detail_respo = detail.choices[0].message.content.strip()
                st.markdown(detail_respo)
