import logging
import math
import os
from decimal import Decimal
from functools import lru_cache
from os import path

import pandas as pd
import pydeck as pdk
import streamlit as st
import yaml
from SPARQLWrapper import get_sparql_dataframe

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@lru_cache
def get_endpoint() -> str:
    config_file = path.join(path.dirname(__file__), os.pardir, "config.yaml")

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sparql_endpoint: str = config["sparql_endpoint"]

    return sparql_endpoint


def map_style_selector() -> str:
    map_styles = {
        pdk.map_styles.CARTO_LIGHT: "Cartographic",
        pdk.map_styles.SATELLITE: "Satellite",
    }
    map_style: str = st.radio(
        "Map style", map_styles.keys(), format_func=lambda x: map_styles[x]
    )

    return map_style


def sparql_query_df(query: str, chunksize=10000) -> pd.DataFrame:
    try:
        chunks = []
        i = 0

        while True:
            query_chunk = query + f"OFFSET {i*chunksize} LIMIT {chunksize}"

            logger.info(
                "Executing SPARQL %s \n", query_chunk
            )  # lazy-% formatting deliberate

            chunk = get_sparql_dataframe(get_endpoint(), query_chunk)
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

        result: pd.DataFrame = pd.concat(chunks, ignore_index=True)

        return result

    except Exception as e:
        # This should be logged instead as calls to this are generally cached
        # st.write("Error in SPARQL Call!")
        raise e


def og_sparql_query_df(query: str) -> pd.DataFrame:
    try:
        return get_sparql_dataframe(get_endpoint(), query)
    except:
        st.write("Error in SPARQL Call!")


def remove_exponent(d):
    """Remove exponent."""
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


# Shamelessly taken from https://github.com/azaitsev/millify
def millify(n, precision=0, drop_nulls=True):
    """Humanize number."""
    millnames = tuple(["", "k", "M", "B", "T", "P", "E", "Z", "Y"])
    n = float(n)

    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )
    result = f"{n / 10 ** (3 * millidx):.{precision}f}"

    if drop_nulls:
        result = remove_exponent(Decimal(result))

    return f"{result}{millnames[millidx]}"
