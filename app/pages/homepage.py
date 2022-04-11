import pandas as pd
import pydeck as pdk
import streamlit as st

from .utils import map_style_selector, millify, sparql_query_df


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
    col1.metric("Amount of observations", millify(get_obs_count(), 1))
    col2.metric("Amount of taxons", millify(get_taxon_count(), 1))
    col3.metric("Amount of locations", millify(get_location_count(), 1))

    locations_layer = pdk.Layer(
        "HeatmapLayer",
        data=locations,
        get_position=["lon", "lat"],
        opacity=0.8,
    )

    view = pdk.data_utils.compute_view(locations[["lon", "lat"]])

    r = pdk.Deck(
        layers=[locations_layer],
        initial_view_state=view,
        map_provider="mapbox",
        map_style=map_style_selector(),
    )

    st.pydeck_chart(r)
