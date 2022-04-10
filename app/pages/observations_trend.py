from datetime import timedelta
from typing import Optional
import pandas as pd
import streamlit as st
from .utils import sparql_query_df


@st.cache
def get_obs_dates(taxon: Optional[str] = None) -> pd.DataFrame:
    if not taxon:
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
        PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
        SELECT * WHERE {
            ?obs a dwc:Occurrence ;
                dwc:eventDate ?date .
        }
        """
    else:
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
        PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
        SELECT * WHERE {{
            ?obs a dwc:Occurrence ;
                a <{taxon}> ;
                dwc:eventDate ?date .
        }}
        """

    df = sparql_query_df(query)
    df["date"] = pd.to_datetime(df["date"])

    return df


@st.cache
def get_all_taxons() -> pd.DataFrame:
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT DISTINCT ?taxon ?name WHERE {
        ?obs a dwc:Occurrence ;
            a ?taxon .
        ?taxon ncbitaxon:has_rank ?rank ;
            rdfs:label ?name .
    }
    """
    df = sparql_query_df(query).set_index("name").sort_index()

    return df


def page_observations_trend():
    st.title("Trend of observations")

    periods = {
        "Yearly": "Y",
        "Monthly": "M",
        "Daily": "D",
    }
    period = periods[st.radio("Period to show", periods.keys(), index=1)]

    with st.spinner():
        observations = get_obs_dates()
        obs_count: pd.Series = observations.resample(period, on="date").size()
        obs_count.rename("count", inplace=True)

    dates = obs_count.index.date
    obs_count.index = dates

    dates_max = dates.max()
    # Show last 20 years by default
    dates_min = dates[dates > dates_max - timedelta(days=365 * 20)].min()

    start_period, end_period = st.select_slider(
        "Period range to show",
        dates,
        value=(max(dates_min, dates.min()), dates_max),
    )

    obs_count = obs_count[
        (obs_count.index >= start_period) & (obs_count.index <= end_period)
    ]
    st.area_chart(obs_count)

    # ---- specific taxon
    st.header("Trend of observations for a specific taxon")

    taxons = get_all_taxons()

    taxon_uri = taxons.loc[st.selectbox("Select taxon", taxons.index)]["taxon"]

    with st.spinner():
        taxon_observations = get_obs_dates(taxon_uri)
        obs_taxon_count: pd.Series = taxon_observations.resample(
            period, on="date"
        ).size()
        obs_taxon_count.rename("count", inplace=True)

    obs_taxon_count.index = obs_taxon_count.index.date
    obs_taxon_count = obs_taxon_count[
        (obs_taxon_count.index >= start_period) & (obs_taxon_count.index <= end_period)
    ]
    st.area_chart(obs_taxon_count)
