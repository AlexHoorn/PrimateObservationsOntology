import pandas as pd
import streamlit as st
from .utils import sparql_query_df


@st.cache
def get_obs_dates():
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT * WHERE {
        ?obs a dwc:Occurrence ;
            a / rdfs:label ?name ;
            dwc:eventDate ?date .
    }
    """
    df = sparql_query_df(query)
    df["date"] = pd.to_datetime(df["date"])

    return df


def page_observations_trend():
    st.title("Trend of observations")

    periods = {
        "Yearly": "Y",
        "Monthly": "M",
        "Daily": "D",
    }
    period = periods[st.radio("Period to show", periods.keys())]

    with st.spinner():
        observations = get_obs_dates()
        obs_count: pd.Series = observations.resample(period, on="date").size()
        obs_count.rename("count", inplace=True)

    dates = obs_count.index.date
    obs_count.index = dates

    start_period, end_period = st.select_slider(
        "Period range to show",
        dates,
        value=(dates.min(), dates.max()),
    )

    obs_count = obs_count[
        (obs_count.index >= start_period) & (obs_count.index <= end_period)
    ]
    st.area_chart(obs_count)
