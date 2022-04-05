import streamlit as st
from pages import pages

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    with st.sidebar:
        page = st.radio("Select page", pages.keys())

    pages[page]()
