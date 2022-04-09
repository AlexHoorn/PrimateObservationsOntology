import pandas as pd
from SPARQLWrapper import QueryResult, SPARQLWrapper, JSON
import streamlit as st
    

def print_query_result(res_obj:QueryResult) ->None:
    json_res = res_obj.convert()
    df_dict = {}

    json_res2 = json_res['results']['bindings']
    
    for res_var in json_res2[0].keys():
        df_dict[res_var] = []

    for i in range(len(json_res2)):
        for res_var in json_res2[i].keys():
            df_dict[res_var].append(json_res2[i][res_var]['value'])
    
    df_res = pd.DataFrame(df_dict)

    st.dataframe(df_res)

def query_db_callback(qry:str,sparql_con:SPARQLWrapper) -> None:
    
    sparql_con.setQuery(qry)
    try:
        res_obj = sparql_con.query()
        print_query_result(res_obj)
    
    except:
        st.write("Query Execution Error!")
    
def sparql_endpoint() -> None:
    
    end_point_url = "https://api.krr.triply.cc/datasets/NathanV/KRWprimatestaxonomy/services/KRWprimatestaxonomy/sparql" #SPARQL Endpoint URL

    sparql_con = SPARQLWrapper(end_point_url)
    sparql_con.setReturnFormat(JSON)

    with st.form("sparql_endpoint_form"):
    
        qry = st.text_area("Type in your SPARQL Query Below : ")

        submitted = st.form_submit_button(label="Try the Query!")
        if (submitted):
            query_db_callback(qry,sparql_con)

    return