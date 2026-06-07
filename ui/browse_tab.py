# Kod: Engelska
# Kommentarer: Svenska
# Browse fliken - bläddra och filtrera termer från PostgreSQL

import streamlit as st
from ui import api


def render():
    """Renderar Browse-tabben. Anropas från streamlit_app.py."""
    st.subheader("Bläddra bland termer")
    st.caption("Filtrerar live mot API't när du skriver.")

    col1, col2 = st.columns(2)
    with col1:
        browse_search = st.text_input(
            "Sök term:", placeholder="loop", key="browse_search"
        )
    with col2:
        browse_category = st.text_input(
            "Filtrera kategori:", placeholder="Python", key="browse_cat"
        )

    try:
        # None om fältet är tomt, api.get_terms ignorerar None-values
        terms = api.get_terms(
            search=browse_search or None,
            category=browse_category or None,
        )

        st.caption(f"{len(terms)} termer")

        for term in terms:
            cats = ", ".join(c["name"] for c in term.get("categories", []))
            label = f"**{term['term']}** · _{cats}_ · `{term['difficulty']}`"
            with st.expander(label):
                st.write(term["definition"])
                sources = term.get("sources", [])
                if sources:
                    st.caption("Källa: " + ", ".join(s["name"] for s in sources))

    except Exception as e:
        st.error(f"Fel vid hämtning av termer: {e}")
