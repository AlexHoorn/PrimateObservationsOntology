from typing import Tuple
import streamlit as st
from .utils import sparql_query_df
import pandas as pd

from .observations_count import get_ranks, get_obs_rank

    
def process_data(df:pd.DataFrame) -> Tuple[list, list]:
    raw_df = df
    raw_df.sort_values(by="name",inplace=True,ignore_index=True)
    raw_df_grouped = raw_df.groupby(by="name")
    df_lst = []
    sub_type_list = []
    for g_name,g_data in raw_df_grouped:
        new_df = raw_df_grouped.get_group(g_name)
        new_df.drop(labels=["name","kind"],inplace=True,axis=1)
        new_df.reset_index(drop=True,inplace=True)
        df_lst.append(new_df)
        sub_type_list.append(str(g_name))

    
    return (sub_type_list, df_lst)


def page_observations_dist() -> None:
    
    ranks = get_ranks()

    rank_name: str = st.selectbox(
        "Select rank",
        options=ranks.index,
        format_func=lambda x: f"{x.title()} - {ranks.loc[x]['count']} observations",
    )
    
    observations = get_obs_rank(ranks.loc[rank_name]["rank"])

    (sub_type_list, df_lst) = process_data(observations)

    st.write(sub_type_list)

    st.dataframe(df_lst[0])

    st.map(df_lst[0])

    return