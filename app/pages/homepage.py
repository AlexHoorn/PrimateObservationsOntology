import pandas as pd
import streamlit as st
from .utils import sparql_query_df


@st.cache
def get_obs_count() -> int:
    query = """
    SELECT (COUNT(?obs) as ?count)
    WHERE {?obs a <http://rs.tdwg.org/dwc/terms/Occurrence>}
    """
    count: int = sparql_query_df(query).iloc[0]["count"]

    return count


@st.cache
def get_taxon_count() -> int:
    query = """
    SELECT (COUNT(?taxon) as ?count)
    WHERE {?taxon <http://purl.obolibrary.org/obo/ncbitaxon#has_rank> ?rank}
    """
    count: int = sparql_query_df(query).iloc[0]["count"]

    return count


@st.cache
def get_location_count() -> int:
    query = """
    SELECT (COUNT(?loc) as ?count)
    WHERE {?loc a <https://www.geonames.org/ontology#Location>}
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
    st.title("🏠 Homepage")
    st.write("⬅ Use the sidebar to navigate our app.")

    locations = get_obs_locs()

    st.header("Summary of observations")

    col1, col2, col3 = st.columns(3)
    col1.metric("Amount of observations", f"{get_obs_count():,}")
    col2.metric("Amount of taxons", f"{get_taxon_count():,}")
    col3.metric("Amount of locations", f"{get_location_count():,}")

    st.map(locations)
