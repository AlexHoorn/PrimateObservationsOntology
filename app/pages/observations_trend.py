from datetime import timedelta
from typing import Optional

import altair as alt
import pandas as pd
import streamlit as st

from .observations_map import get_ranks
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
            <{taxon}> rdfs:label ?taxonName .
        }}
        """

    df = sparql_query_df(query)
    df["date"] = pd.to_datetime(df["date"])

    return df


@st.cache
def get_taxons(rank: str) -> pd.DataFrame:
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT DISTINCT ?taxon ?name WHERE {{
        ?obs a dwc:Occurrence ;
            a ?taxon .
        ?taxon ncbitaxon:has_rank <{rank}> ;
            rdfs:label ?name .
    }}
    """
    df = sparql_query_df(query).set_index("name").sort_index()

    return df


def page_observations_trend():
    st.title("Trend of observations")
    col1, col2 = st.columns(2)

    # Period aggregation to choose
    periods = {
        "Yearly": "Y",
        "Monthly": "M",
        "Daily": "D",
    }
    period = periods[col1.radio("Period to show", periods.keys(), index=1)]

    # Yearly count
    observations = get_obs_dates()
    obs_count: pd.Series = (
        observations.resample(period, on="date").size().rename("count")
    )

    # Cumulative
    cumulative = col2.radio("Cumulative", [True, False])
    if cumulative:
        obs_count = obs_count.cumsum()

    # Determine date range to show
    dates = obs_count.index.date
    obs_count.index = dates
    dates_max = dates.max()
    # Show last 20 years by default
    dates_min = dates[dates > dates_max - timedelta(days=365 * 20)].min()
    # Selector
    start_period, end_period = st.select_slider(
        "Period range to show",
        dates,
        value=(max(dates_min, dates.min()), dates_max),
    )
    # Filter between range
    obs_count = obs_count[
        (obs_count.index >= start_period) & (obs_count.index <= end_period)
    ]

    # Show the chart
    st.area_chart(obs_count)

    # ---- For specific taxons
    st.header("For specific taxons")

    # Show from specific rank
    ranks = get_ranks()
    ranks_select = st.selectbox(
        "Show taxons from rank",
        ranks.index,
        format_func=lambda x: ranks.loc[x, "title"],
        index=2,
    )
    taxons = get_taxons(ranks.loc[ranks_select]["rank"])

    # Select taxons to show
    taxon_uris = taxons.loc[
        st.multiselect(
            "Select taxons", taxons.index, default=taxons.index[:10].tolist()
        )
    ]["taxon"]

    # Select all if selection is empty
    if len(taxon_uris) == 0:
        taxon_uris = taxons["taxon"].tolist()

    # Collect observations for selected taxons
    taxons_observations = [get_obs_dates(taxon) for taxon in taxon_uris]

    # This looks like shit but does what it must
    # Essentially gets us a dataframe with the observations per taxon for the set period
    # and makes sure any empty periods are filled with 0 to not screw with the cumulative visualisation
    taxons_count = (
        pd.concat(taxons_observations)
        .groupby("taxonName")
        .resample(period, on="date")
        .size()
    )
    if len(taxons_observations) == 1:
        taxons_count = taxons_count.stack()
    taxons_count = taxons_count.rename("count")
    taxons_count = (
        taxons_count.reset_index()
        .pivot(index="taxonName", columns="date", values="count")
        .fillna(0)
        .stack()
    )
    if cumulative:
        taxons_count = taxons_count.groupby("taxonName").cumsum()
    taxons_count = taxons_count.rename("count").reset_index()

    # Convert to dates instead of datetimes
    taxons_count["date"] = taxons_count["date"].dt.date
    # Only keep in between given range
    taxons_count = taxons_count[
        (taxons_count["date"] >= start_period) & (taxons_count["date"] <= end_period)
    ]

    # Create the chart
    chart = (
        alt.Chart(taxons_count)
        .mark_area()
        .encode(
            x="date:T",
            y="count:Q",
            color=alt.Color("taxonName"),
            tooltip=["taxonName", "count", "date"],
        )
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
