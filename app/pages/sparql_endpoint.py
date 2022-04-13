import streamlit as st

from .utils import og_sparql_query_df


def query_db_callback(qry: str) -> None:

    res_obj = og_sparql_query_df(qry)
    st.dataframe(res_obj)


def page_sparql_endpoint() -> None:

    with st.form("sparql_endpoint_form"):

        qry = st.text_area("Type in your SPARQL Query Below : ")

        submitted = st.form_submit_button(label="Try the Query!")
        if submitted:
            query_db_callback(qry)

    return
