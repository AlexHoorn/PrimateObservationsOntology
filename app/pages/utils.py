import os
from os import path

import yaml
from pandas import DataFrame
from SPARQLWrapper import get_sparql_dataframe

config_file = path.join(path.dirname(__file__), os.pardir, "config.yaml")

with open(config_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

sparql_endpoint: str = config["sparql_endpoint"]


def sparql_query_df(query: str) -> DataFrame:
    return get_sparql_dataframe(sparql_endpoint, query)
