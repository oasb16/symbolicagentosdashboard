# AGENDΔ_CORE Symbolic Memory Dashboard

This Streamlit dashboard dynamically loads symbolic agendas from a persistent memory file and fetches GPT-aligned summaries using identity-bound prompts.

## 💡 Key Features

- Secure, symbolic agenda persistence (`agenda_store.json`)
- Stateless OpenAI API prompt injection with symbolic memory
- Safe prompt structure that avoids policy flags or hallucination
- Fully Streamlit deployable

## 🚀 Run

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```
