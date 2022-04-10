from pandas import DataFrame
import streamlit as st

from .utils import sparql_query_df


@st.cache
def get_ranks() -> DataFrame:
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT ?rank ?rankLabel (COUNT(?rank) as ?count) WHERE {
        ?obs a dwc:Occurrence ;
            a / ncbitaxon:has_rank ?rank .
        ?rank rdfs:label ?rankLabel .
    }
    GROUP BY ?rank ?rankLabel
    """
    df = (
        sparql_query_df(query)
        .set_index("rankLabel")
        .sort_values("count", ascending=False)
    )

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

    return df


def page_observations_count():
    st.title("📊 Observation counts")

    # Ranks and their counts of observations
    ranks = get_ranks()

    col1, col2 = st.columns([1, 1])

    with col1:
        # Select rank to list
        rank_name: str = st.selectbox(
            "Select rank",
            options=ranks.index,
            format_func=lambda x: f"{x.title()} - {ranks.loc[x]['count']} observations",
            index=ranks.index.tolist().index("species"),
        )

    # Get the observations for selected rank
    observations = get_obs_rank(ranks.loc[rank_name]["rank"])
    # Count of occurences
    obs_counts = observations["name"].value_counts()

    with col2:
        # Select amount to list
        n_kinds = observations["name"].nunique()
        if n_kinds > 1:
            top_n: int = st.slider(
                "Show top amount", 1, n_kinds, value=min(25, n_kinds)
            )
        else:
            top_n = 1

    # Barplot of counts
    if top_n > 1:
        st.bar_chart(obs_counts[:top_n])

    st.header("Map of observations")

    # Select the kinds to show on the map
    kinds = st.multiselect(
        f"Select {rank_name}",
        sorted(observations["name"].unique()),
        default=obs_counts[:top_n].index.tolist(),
    )
    # Show the map
    st.map(observations[observations["name"].isin(kinds)])
