import streamlit as st

indexes = ("rihappy", "amazon")


def search_bar() -> None:
    search_col, index_col = st.columns([3, 1])

    with search_col:
        yield st.text_input(label="", placeholder="Search something")

    with index_col:
        yield st.selectbox(label="", options=indexes)
