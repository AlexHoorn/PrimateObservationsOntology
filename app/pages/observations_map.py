import colorcet as cc
import numpy as np
import pydeck as pdk
import streamlit as st
from pandas import DataFrame, Series

from .utils import map_style_selector, sparql_query_df


@st.cache
def get_ranks() -> DataFrame:
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT ?rank ?rankLabel
        (COUNT(?rank) as ?count)
        (COUNT(DISTINCT ?kind) as ?kindCount)
    WHERE {
        ?obs a dwc:Occurrence ;
            a ?kind.
        ?kind ncbitaxon:has_rank ?rank .
        ?rank rdfs:label ?rankLabel .
    }
    GROUP BY ?rank ?rankLabel
    HAVING (?kindCount > 1 || ?rankLabel = "order")
    ORDER BY DESC(?count) ASC(?kindCount)
    """
    df = sparql_query_df(query).set_index("rankLabel")
    df["title"] = df.apply(format_rank_title, axis=1)

    return df


@st.cache
def get_obs_rank(rank: str) -> DataFrame:
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT * WHERE {{
        ?obs a dwc:Occurrence ;
            a ?kind .
        ?kind ncbitaxon:has_rank <{rank}> ;
            rdfs:label ?name .

        OPTIONAL{{?obs dwc:decimalLatitude ?lat}}
        OPTIONAL{{?obs dwc:decimalLongitude ?lon}}
    }}
    """
    df = sparql_query_df(query)
    df["name"] = df["name"].astype("category")

    return df


def format_rank_title(rank: Series) -> str:
    return (
        f"{rank.name.title()}: "
        + f"{rank['count']} observations, "
        + f"{rank['kindCount']} taxons"
    )


def page_observations_count():
    st.title("🌍 Observation Map")

    # Ranks and their counts of observations
    ranks = get_ranks()

    col1, col2 = st.columns([1, 1])

    with col1:
        # Select rank to list
        rank_name: str = st.selectbox(
            "Select rank",
            options=ranks.index,
            format_func=lambda x: ranks.loc[x, "title"],
            index=ranks.index.tolist().index("species"),
        )

    # Get the observations for selected rank
    observations = get_obs_rank(ranks.loc[rank_name]["rank"])

    with col2:
        # Select amount to list
        n_kinds = int(ranks.loc[rank_name]["kindCount"])
        if n_kinds > 1:
            top_n: int = st.slider(
                "Show top amount", 1, n_kinds, value=min(25, n_kinds)
            )
        else:
            top_n = 1

    if top_n > 1:
        # Barplot of counts
        st.bar_chart(observations["name"].value_counts()[:top_n])

    # Select the kinds to show on the map
    kinds = st.multiselect(
        f"Show only {rank_name}",
        sorted(observations["name"].unique()),
    )

    if kinds:
        observations = observations[observations["name"].isin(kinds)].copy()
    else:
        observations = observations.copy()

    # Create the map properties
    view = pdk.data_utils.compute_view(observations[["lon", "lat"]])
    # Not sexy but gets the job done with decent performance and makes the colors consistent
    color_map = np.array(cc.glasbey_bw) * 255
    observations["color"] = observations["name"].cat.codes.apply(
        lambda x: color_map[x].tolist()
    )

    observations_layer = pdk.Layer(
        "ScatterplotLayer",
        data=observations,
        get_position=["lon", "lat"],
        pickable=True,
        opacity=0.8,
        radius_min_pixels=3,
        get_fill_color="color",
    )

    # Create the actual map
    r = pdk.Deck(
        layers=[observations_layer],
        initial_view_state=view,
        map_provider="mapbox",
        map_style=map_style_selector(),
        tooltip={"text": "{name}"},
    )

    # Show the map
    st.pydeck_chart(r)
