import streamlit as st
from firebase_rtdb import firebase_ref

from st_pages import add_page_title, get_nav_from_toml

nav = get_nav_from_toml(".streamlit/pages.toml")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()