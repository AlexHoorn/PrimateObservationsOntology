import pandas as pd
import streamlit as st
from os import path

# Uses CSV in this example, shouldn't later on
@st.cache
def load_data() -> pd.DataFrame:
    file_path = path.join(path.dirname(__file__), "data", "obs_data_taxon_ID.csv")
    df = pd.read_csv(file_path, index_col=0)
    df.rename({"latitude": "lat", "longitude": "lon"}, axis=1, inplace=True)

    return df


def page_map_all():
    with st.spinner("Loading data"):
        df = load_data()

    st.title("Overview of Observations")
    st.write(f"Data contains {len(df)} observations of Primates.")
    st.map(df)
