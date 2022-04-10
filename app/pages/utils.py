import os
from os import path

import yaml
import pandas as pd
from SPARQLWrapper import get_sparql_dataframe

config_file = path.join(path.dirname(__file__), os.pardir, "config.yaml")

with open(config_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

sparql_endpoint: str = config["sparql_endpoint"]


def sparql_query_df(query: str, chunksize=10000) -> pd.DataFrame:
    chunks = []
    i = 0

    while True:
        query_chunk = query + f"OFFSET {i*chunksize} LIMIT {chunksize}"
        chunk = get_sparql_dataframe(sparql_endpoint, query_chunk)
        curr_size = len(chunk)

        if curr_size > 0:
            chunks.append(chunk)
        else:
            # Break if we get an empty result
            break

        if curr_size < chunksize:
            # Break if we are at the last page
            break

        i += 1

    result: pd.DataFrame = pd.concat(chunks)

    return result
