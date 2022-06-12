import os

import streamlit as st
from meilisearch.client import Client

from components.search_bar import search_bar
from components.search_result import search_result

st.set_page_config(layout="wide", page_icon="📗")

query, index = search_bar()

client = Client(os.environ["MEILISEARCH_URL"], api_key=os.environ["MEILISEARCH_KEY"])
result = client.index(uid=index).search(query=query)

search_result(result)
