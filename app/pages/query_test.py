import streamlit as st

from .utils import sparql_query_df


def page_query_test():
    df = sparql_query_df("SELECT * WHERE {?s ?p ?o}")
    st.write(df)
