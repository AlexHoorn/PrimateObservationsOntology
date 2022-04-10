from datetime import date, timedelta
import pandas as pd
import streamlit as st
from .utils import sparql_query_df


@st.cache
def get_obs_dates() -> pd.DataFrame:
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon#>
    PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
    SELECT * WHERE {
        ?obs a dwc:Occurrence ;
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
