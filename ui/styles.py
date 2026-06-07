# Kod: Engelska
# Kommentarer: Svenska
# CSS-stilar som en funktion - anropas en gång från streamlit_app.py

import streamlit as st

_CSS = """
<style>
    .source-tag {
        display: inline-block;
        background-color: #1e3a5f;
        color: #90caf9;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        margin: 2px 3px;
        font-family: monospace;
    }
    .answer-box {
        background-color: #0d1b2a;
        border-left: 3px solid #2196f3;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        font-size: 0.97rem;
        line-height: 1.6;
    }
</style>
"""


def inject():
    """Injicerar CSS i Streamlit-sidan. Anropas en gång i streamlit_app.py."""
    st.markdown(_CSS, unsafe_allow_html=True)
