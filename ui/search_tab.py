# Kod: Engelska
# Kommentarer: Svenska
# Search fliken, semantisk sökning direkt mot ChromaDB

import streamlit as st
from ui import api


def render():
    """Renderar Search-tabben. Anropas från streamlit_app.py."""
    st.subheader("Semantisk sökning")
    st.caption(
        "Söker direkt i vektordatabasen (ChromaDB) utan LLM. "
        "Lägre distans = bättre träff."
    )

    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Sökterm:",
            placeholder="exception handling",
            key="search_input",
        )
    with col2:
        k = st.slider("Träffar", min_value=1, max_value=10, value=5)

    if st.button("Sök", type="primary", key="search_btn"):
        if not query.strip():
            st.warning("Skriv ett sökord.")
            return

        with st.spinner("Söker i vektordatabasen..."):
            try:
                results = api.search(query, k)

                if not results:
                    st.info("Inga träffar.")
                    return

                for res in results:
                    label = (
                        f"**{res['term']}** - "
                        f"`{res['slug']}` "
                        f"(distans: {res['distance']})"
                    )
                    with st.expander(label):
                        st.write(res["snippet"])
                        if res.get("sources"):
                            st.caption("Källa: " + ", ".join(res["sources"]))

            except Exception as e:
                st.error(f"Fel: {e}")
