import streamlit as st

st.set_page_config(layout="wide", page_icon="📗")

with open("README.md", "r") as f:
    st.markdown(f.read())
