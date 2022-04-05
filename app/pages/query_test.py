import pandas as pd
import streamlit as st
from rdflib import ConjunctiveGraph


def page_query_test():
    g = ConjunctiveGraph()
    res = g.query(
        """
        SELECT * WHERE {
        SERVICE <https://api.triplydb.com/datasets/weiyuxinghen/primate-database/services/primate-database/sparql> {
            ?s ?p ?o
            }
        }
        """,
    )

    df = pd.DataFrame(res)
    st.dataframe(df)
