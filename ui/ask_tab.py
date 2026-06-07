# Kod: Engelska
# Kommentarer: Svenska
# Ask tab, RAG-assistenten med source tracking

import requests
import streamlit as st
from ui import api


def render():
    """Renderar Ask-tabben. Anropas från streamlit_app.py."""
    st.subheader("Fråga din Data Engineering-assistent")
    st.caption(
        "Svar baseras **enbart** på ordlistans innehåll - "
        "inga hallucinationer. Källorna visas alltid."
    )

    question = st.text_input(
        "Din fråga:",
        placeholder="What does DRY stand for?  /  Vad är en nested loop?",
        key="ask_input",
    )

    if st.button("Fråga", type="primary", key="ask_btn"):
        if not question.strip():
            st.warning("Skriv en fråga först.")
            return

        with st.spinner("Hämtar kontext och genererar svar..."):
            try:
                data = api.ask(question)

                # === Svar ===
                st.markdown("**Svar:**")
                st.markdown(
                    f'<div class="answer-box">{data["answer"]}</div>',
                    unsafe_allow_html=True,
                )

                # === Källor som pill-taggar ===
                if data.get("sources"):
                    st.markdown("<br>**Använd kontext från:**", unsafe_allow_html=True)
                    tags = "".join(
                        f'<span class="source-tag">{s}</span>' for s in data["sources"]
                    )
                    st.markdown(tags, unsafe_allow_html=True)

            except requests.exceptions.Timeout:
                st.error("LLM-anropet tog för lång tid. Försök igen.")
            except Exception as e:
                st.error(f"Fel: {e}")
