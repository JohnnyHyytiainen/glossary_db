# Kod: Engelska
# Kommentarer: Svenska
import streamlit as st
from ui import styles
from ui import ask_tab, search_tab, browse_tab
from ui.api import health_check

# Entry point för Streamlit-appen.
# Enda ansvar: sätt upp sidan, kolla health, skapa tabbar, anropa render().
# Ingen logik, ingen CSS, inga API-anrop här.

# ===== Sidkonfiguration =====
st.set_page_config(
    page_title="Glossary DB",
    page_icon="",
    layout="centered",
)

styles.inject()

# ===== Header =====
st.title("Glossary DB")
st.caption("Data Engineering-ordlista med semantisk sökning och AI-assistent")

# ===== Health check, stoppa appen om API't inte svarar =====
if not health_check():
    st.error(
        "**API:et svarar inte.** Starta servern i en annan terminal:\n\n"
        "`uv run uvicorn src.main:app --reload`"
    )
    st.stop()

st.success("API anslutet")
st.divider()

# ===== Tabs - varje tab fil har sin egen renderings logik =====
tab_ask, tab_search, tab_browse = st.tabs(
    [
        "🤖 Fråga assistenten",
        "🔍 Semantisk sökning",
        "📖 Bläddra termer",
    ]
)

with tab_ask:
    ask_tab.render()

with tab_search:
    search_tab.render()

with tab_browse:
    browse_tab.render()
