import streamlit as st
from pages import pages

# To run this make sure you have streamlit installed and run `streamlit run app.py`
if __name__ == "__main__":
    st.set_page_config(layout="wide")

    with st.sidebar:
        page: str = st.radio("Select page", pages.keys())

    pages[page]()
