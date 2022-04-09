import streamlit as st

from .utils import sparql_query


def page_query_test():
    df = sparql_query("SELECT * WHERE {?s ?p ?o}")
    st.write(df)
