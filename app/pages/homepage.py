import pandas as pd
import streamlit as st
from .utils import sparql_query_df


@st.cache
def get_obs_count() -> int:
    query = """
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT (COUNT(?obs) as ?count) WHERE {
        ?obs a dwc:Occurrence .
    }
    """
    count: int = sparql_query_df(query).iloc[0]["count"]

    return count


@st.cache
def get_obs_locs() -> pd.DataFrame:
    query = """
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT * WHERE {
        ?obs a dwc:Occurrence .
        OPTIONAL{?obs dwc:decimalLatitude ?lat}
        OPTIONAL{?obs dwc:decimalLongitude ?lon}
    }
    """
    df = sparql_query_df(query)

    return df


def page_home():
    with st.spinner("Loading data"):
        count = get_obs_count()
        df = get_obs_locs()

    st.title("🏠 Homepage")
    st.write("⬅ Use the sidebar to navigate our app.")

    st.header("Map of all observations")
    st.write(f"Data contains {count} observations of Primates.")
    st.map(df)
