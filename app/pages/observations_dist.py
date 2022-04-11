from typing import Tuple
import streamlit as st
from .utils import sparql_query_df
import pandas as pd
import numpy as np

from haversine import haversine

from .observations_count import get_ranks, get_obs_rank


def split_into_groups(df:pd.DataFrame) -> Tuple[list, list]:
    raw_df = df.copy()
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


def ret_mat_dist(pts_list:list) -> np.ndarray:
    m = len(pts_list)
    ans = np.zeros((m,m))
    for i in range(m):
        for j in range(i+1,m):
            ans[i,j] = haversine(pts_list[i],pts_list[j])

    ans = np.add(ans,np.transpose(ans))
    return ans

def get_max_idx(ar:np.ndarray) -> Tuple[list,float]:
    max_ele_idx = np.where(ar == np.amax(ar))
    dist = ar[max_ele_idx[0][0],max_ele_idx[0][1]]
    idx_list = [max_ele_idx[0][0],max_ele_idx[0][1]]
    return (idx_list,dist)


def get_max_dist_obs(df:pd.DataFrame) -> pd.DataFrame:
    lst_points = [(x,y) for x,y in zip(df['lat'],df['lon'])]

    dist_mat = ret_mat_dist(lst_points)
    st.header("Distance Calculation Matrix : ")
    st.write(dist_mat)
    (max_idx,max_dist) = get_max_idx(dist_mat)
    
    row1 = df.iloc[max_idx[0]]
    row2 = df.iloc[max_idx[1]]

    dict_temp ={"ObservationID":[row1['obs'],row2['obs']],
    "lat":[row1['lat'],row2['lat']],
    "lon":[row1['lon'],row2['lon']],
    "Distance":[max_dist,max_dist]}
    

    ans_df=pd.DataFrame(dict_temp)
    return ans_df


def page_observations_dist() -> None:
    
    st.title("Observations Distribution")
    
    ranks = get_ranks()

    col1, col2 = st.columns([1,1])

    with col1:
        rank_name: str = st.selectbox(
            "Select rank",
            options=ranks.index,
            format_func=lambda x: f"{x.title()} - {ranks.loc[x]['count']} observations",
        )
    
    observations = get_obs_rank(ranks.loc[rank_name]["rank"])

    (sub_type_list, df_lst) = split_into_groups(observations)
    
    with col2:
        sub_type_select = st.selectbox(
            f"Select {rank_name}",
            options=sub_type_list
        )
    
    with st.form("calc_obs_dist"):
        
        submitted = st.form_submit_button(label="Show Farthest Observations!")

        if(submitted):
            final_res = get_max_dist_obs(df_lst[sub_type_list.index(sub_type_select)])
        
            st.header("Observation Details : ")
            st.write(f"Distance : {round(final_res['Distance'].values[0],3)} Km")
            st.dataframe(final_res)
            st.header("Visualisation on Map : ")
            st.map(final_res)

    return