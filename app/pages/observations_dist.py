from typing import Tuple

import colorcet as cc
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
from haversine import haversine

from .observations_map import get_obs_rank, get_ranks
from .utils import map_style_selector, logger


def split_into_groups(df: pd.DataFrame) -> Tuple[list, list]:
    raw_df = df.copy()
    raw_df.sort_values(by="name", inplace=True, ignore_index=True)
    raw_df_grouped = raw_df.groupby(by="name")
    df_lst = []
    sub_type_list = []
    for g_name, g_data in raw_df_grouped:
        new_df = raw_df_grouped.get_group(g_name)
        new_df.drop(labels=["name", "kind"], inplace=True, axis=1)
        new_df.reset_index(drop=True, inplace=True)
        df_lst.append(new_df)
        sub_type_list.append(str(g_name))

    return (sub_type_list, df_lst)


def ret_mat_dist(pts_list: list) -> np.ndarray:
    
    m = len(pts_list)
    logger.info(
        f"Calculating Distance Matrix, Size : {m} by {m}"
    )
    ans = np.zeros((m, m))
    for i in range(m):
        for j in range(i + 1, m):
            ans[i, j] = haversine(pts_list[i], pts_list[j])

    #ans = np.add(ans, np.transpose(ans))
    logger.info(
        "Distance Matrix Calculated"
    )
    return ans


def get_max_ele(ar: np.ndarray) -> Tuple[list, float]:
    max = ar[0, 0]
    (m, n) = ar.shape
    max_idx = [0, 0]
    for i in range(m):
        for j in range(i + 1, n):
            if ar[i, j] > max:
                max = ar[i, j]
                max_idx = [i, j]

    return (max_idx, max)


def get_max_dist_obs(df: pd.DataFrame) -> pd.DataFrame:

    lst_points = [(x, y) for x, y in zip(df["lat"], df["lon"])]

    dist_mat = ret_mat_dist(lst_points)

    (max_idx, max_dist) = get_max_ele(dist_mat)

    row1 = df.iloc[max_idx[0]]
    row2 = df.iloc[max_idx[1]]

    dict_temp = {
        "ObservationID": [row1["obs"], row2["obs"]],
        "lat": [row1["lat"], row2["lat"]],
        "lon": [row1["lon"], row2["lon"]],
        "Distance": [max_dist, max_dist],
    }

    ans_df = pd.DataFrame(dict_temp)
    return ans_df


def page_observations_dist() -> None:

    pd.set_option("mode.chained_assignment", None)

    st.title("🔃 Observations Spread")

    ranks = get_ranks()

    ranks = ranks[ranks["kindCount"] > 10]

    rank_name: str = st.selectbox(
        "Select Rank : ",
        options=ranks.index,
        format_func=lambda x: f"{x.title()} - {ranks.loc[x]['count']} observations, {ranks.loc[x]['kindCount']} taxons",
    )

    observations = get_obs_rank(ranks.loc[rank_name]["rank"])

    (sub_type_list, df_lst) = split_into_groups(observations)

    col1, col2 = st.columns([1, 1])

    with col1:
        sub_type_select = st.selectbox(
            f"Select {rank_name.title()} 1 : ", options=sub_type_list
        )

    with col2:
        sub_type_select2 = st.selectbox(
            f"Select {rank_name.title()} 2 : ", options=sub_type_list
        )

    if sub_type_select != sub_type_select2:
        final_res = get_max_dist_obs(df_lst[sub_type_list.index(sub_type_select)])
        final_res2 = get_max_dist_obs(df_lst[sub_type_list.index(sub_type_select2)])
    else:
        final_res = get_max_dist_obs(df_lst[sub_type_list.index(sub_type_select)])
        final_res2 = final_res.copy()

    final_res3 = pd.concat([final_res, final_res2], ignore_index=True)

    final_res3.insert(
        len(final_res3.columns),
        "order_no",
        [sub_type_select, sub_type_select, sub_type_select2, sub_type_select2],
    )

    final_res3 = final_res3.astype({"order_no": "category"})

    st.header(
        f"Comparison of Max Spread between {sub_type_select.title()} and {sub_type_select2.title()} :"
    )

    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown(f"**{rank_name.title()} Name : {sub_type_select.title()}**")
        st.markdown(f"**Max Distance : {round(final_res['Distance'].values[0],3)} Km**")
        final_res.drop("Distance", inplace=True, axis=1)
        st.dataframe(final_res)

    with col4:
        st.markdown(f"**{rank_name.title()} Name : {sub_type_select2.title()}**")
        st.markdown(
            f"**Max Distance : {round(final_res2['Distance'].values[0],3)} Km**"
        )
        final_res2.drop("Distance", inplace=True, axis=1)
        st.dataframe(final_res2)

    st.header("Visualisation on Map : ")

    # Create the map properties
    view = pdk.data_utils.compute_view(final_res3[["lon", "lat"]])
    # Not sexy but gets the job done with decent performance and makes the colors consistent
    color_map = np.array(cc.glasbey_bw) * 255
    final_res3["color"] = final_res3["order_no"].cat.codes.apply(
        lambda x: color_map[x].tolist()
    )

    observations_layer = pdk.Layer(
        "ScatterplotLayer",
        data=final_res3,
        get_position=["lon", "lat"],
        pickable=True,
        opacity=0.8,
        radius_min_pixels=3,
        get_fill_color="color",
    )

    r = pdk.Deck(
        layers=[observations_layer],
        initial_view_state=view,
        map_provider="mapbox",
        map_style=map_style_selector(),
        tooltip={"text": "{order_no}"},
    )

    st.pydeck_chart(r)

    return
