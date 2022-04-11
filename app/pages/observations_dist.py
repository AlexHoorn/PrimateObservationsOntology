from typing import Tuple
import streamlit as st
from .utils import sparql_query_df
import pandas as pd
import numpy as np

from .observations_count import get_ranks, get_obs_rank


def split_into_groups(df:pd.DataFrame) -> Tuple[list, list]:
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

def idx_max(lst:list) -> int:
    idx=0
    max=lst[0]
    for ele in lst:
        if ele>max:
            idx=lst.index(ele)
            max=lst[idx]
    
    return idx

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def calc_max_dist(df:pd.DataFrame) -> pd.DataFrame:
    p_df = df
    #p_list = [[lat,lon] for lat,lon in zip(p_df['lat'],p_df['lon'])]
    p_lon = [lon for lon in p_df['lon']]
    p_lat = [lat for lat in p_df['lat']]
    max_d_list = []
    max_p2_lat = []
    max_p2_lon = []
    max_obs_name = []
    for i in range(len(p_lon)):
        t_list_lon = []
        t_list_lat = []
        for j in range(len(p_lon)):
            t_list_lat.append(p_lat[i])
            t_list_lon.append(p_lon[i])
        
        d_list = haversine_np(t_list_lon,t_list_lat,p_lon,p_lat)
        
        idx = idx_max(d_list.tolist())
        max_d_list.append(d_list[idx])
        max_p2_lat.append(p_lat[idx])
        max_p2_lon.append(p_lon[idx])
        max_obs_name.append(p_df.iloc[idx]['obs'])

    p_df.insert(len(p_df.columns),column="Max Distance",value=max_d_list)
    p_df.insert(len(p_df.columns),column="2nd Point ObsId",value=max_obs_name)
    p_df.insert(len(p_df.columns),column="2nd Point Lat",value=max_p2_lat)
    p_df.insert(len(p_df.columns),column="2nd Point Lon",value=max_p2_lon)

    return p_df

def get_max_dist_entry(df:pd.DataFrame) -> pd.DataFrame:
    res = df.iloc[[df['Max Distance'].idxmax()]]
    t_dict={"Observation ID":[res['obs'].values[0],res['2nd Point ObsId'].values[0]],
    "lat":[res['lat'].values[0],res['2nd Point Lat'].values[0]],
    "lon":[res['lon'].values[0],res['2nd Point Lon'].values[0]],
    "Distance":[res['Max Distance'].values[0],res['Max Distance'].values[0]]}
    final_res = pd.DataFrame(data=t_dict)
    return final_res


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
            df_with_dist = calc_max_dist(df_lst[sub_type_list.index(sub_type_select)])
        
            
            final_res = get_max_dist_entry(df_with_dist)

            st.header("Observation Details : ")
            st.write(f"Distance : {round(final_res['Distance'].values[0],3)} Km")
            st.dataframe(final_res)
            st.header("Visualisation on Map : ")
            st.map(final_res)

    return