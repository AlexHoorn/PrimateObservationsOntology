import os
from os import path

import yaml
from pandas import DataFrame
from SPARQLWrapper import get_sparql_dataframe
import pandas as pd
import streamlit as st

config_file = path.join(path.dirname(__file__), os.pardir, "config.yaml")

with open(config_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

sparql_endpoint: str = config["sparql_endpoint"]


def sparql_query_df(query: str) -> DataFrame:
    
    try:
        l_retdf = []
        i=0

        while(True):
            qry = query + f"offset {i} limit 10000"
            
            df = get_sparql_dataframe(sparql_endpoint, qry)
            
            if(len(df) > 0):
                l_retdf.append(df)
            else:
                break
            i+=10000

        for df in l_retdf[1:]:
            l_retdf[0] = pd.concat(objs=[l_retdf[0],df],ignore_index=True)

        return l_retdf[0]

    except:
        st.write("Error in SPARQL Call!")


def og_sparql_query_df(query:str) -> DataFrame:
    try:
        return get_sparql_dataframe(sparql_endpoint,query)
    except:
        st.write("Error in SPARQL Call!")

