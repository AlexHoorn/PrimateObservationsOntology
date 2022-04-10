from typing import Tuple
import streamlit as st
from .utils import sparql_query_df
import pandas as pd

from .observations_count import get_ranks, get_obs_rank

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_data() -> pd.DataFrame:
    ranks = get_ranks()

    

@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def process_data(df:pd.DataFrame) -> Tuple[list, list]:
    raw_df = df
    raw_df.sort_values(by="ncbi_taxon_name",inplace=True,ignore_index=True)
    raw_df_grouped = raw_df.groupby(by="ncbi_taxon_name")
    df_lst = []
    species_list = []
    for g_name,g_data in raw_df_grouped:
        new_df = raw_df_grouped.get_group(g_name)
        new_df.drop(labels="ncbi_taxon_name",inplace=True,axis=1)
        new_df.reset_index(drop=True,inplace=True)
        df_lst.append(new_df)
        species_list.append(str(g_name))

    
    return (species_list, df_lst)


def distribution_obs() -> None:
    
    ranks = get_ranks()
    st.write(ranks)


    #(s_list,p_df_list) = process_data(obs_df)
    #s_list_2_df = get_ranks()
    #st.dataframe(s_list_2_df)
    #st.write(len(s_list))
    #new_str = ""
    #for type in s_list:
    #    new_str += type+" , "
    #st.write(new_str)
    return