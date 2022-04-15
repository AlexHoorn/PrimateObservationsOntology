# NOTE
# If you wish to run this file then you will need to manually download allCountries.txt and hierarchy.txt
# from the GeoNames download server: https://download.geonames.org/export/dump/
import logging
from os import path

import pandas as pd
from rdflib import OWL, RDF, RDFS, ConjunctiveGraph, Literal, Namespace
from tqdm import tqdm


# Functions to add information from pandas series
def add_relation(row: pd.Series, g: ConjunctiveGraph, ns: Namespace) -> None:
    s = getattr(ns, str(row.childId))
    o = getattr(ns, str(row.parentId))

    g.add((s, ns.partOf, o))


def add_country(row: pd.Series, g: ConjunctiveGraph, ns: Namespace) -> None:
    s = getattr(ns, str(row.name))

    g.add((s, RDF.type, ns.Location))
    g.add((s, RDFS.label, Literal(row["name"])))
    g.add((s, ns.countryCode, Literal(row["country code"])))
    g.add((s, ns.latitude, Literal(row["latitude"])))
    g.add((s, ns.longitude, Literal(row["longitude"])))
    g.add((s, ns.featureClass, Literal(row["feature class"])))
    g.add((s, ns.featureCode, Literal(row["feature code"])))


logging.basicConfig(
    format="%(asctime)s %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
)

base_dir = path.dirname(__file__)
countries_file = path.join(base_dir, "allCountries.txt")
relations_file = path.join(base_dir, "hierarchy.txt")

# Load dataframe of all geonames entities (~12mil rows)
all_countries_cols = [
    "geonameid",
    "name",
    "asciiname",
    "alternatenames",
    "latitude",
    "longitude",
    "feature class",
    "feature code",
    "country code",
    "cc2",
    "admin1 code",
    "admin2 code",
    "admin3 code",
    "admin4 code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification date",
]


if __name__ == "__main__":
    # Download allCountries.txt from https://download.geonames.org/export/dump/
    logging.info("Loading allCountries dataframe")
    countries = pd.read_csv(
        countries_file, sep="\t", names=all_countries_cols, index_col=0
    )

    # Keep only features we are interested in: http://www.geonames.org/export/codes.html
    keep_features = ["A", "H", "L", "P", "T", "U", "V"]

    n_before = len(countries)
    countries = countries[countries["feature class"].isin(keep_features)]

    logging.info(f"Filtered {n_before - len(countries)} unnecessary rows")

    # Load dataframe of all geonames hierarchy relations
    logging.info("Loading relations dataframe")
    # Download hierarchy.txt from https://download.geonames.org/export/dump/
    relations = pd.read_csv(
        relations_file, sep="\t", names=["parentId", "childId", "type"]
    )

    # Only keep relations also in countries dataframe
    relations = relations[
        relations["parentId"].isin(countries.index)
        & relations["childId"].isin(countries.index)
    ]

    # Only keep countries for which we have relations
    countries = countries[
        countries.index.isin(relations["parentId"])
        | countries.index.isin(relations["childId"])
    ]

    # Create new empty graph
    logging.info("Setting up new graph")
    g = ConjunctiveGraph()
    gn = Namespace("http://www.geonames.org/ontology#")

    g.namespace_manager.bind("gn", gn)

    # Make partOf transitive
    g.add((gn.partOf, RDF.type, OWL.TransitiveProperty))

    # Add entity information to graph
    tqdm.pandas(desc="Adding general subject information")
    _ = countries.progress_apply(add_country, axis=1, g=g, ns=gn)

    # Add hierarchical relations
    tqdm.pandas(desc="Adding partOf relations")
    _ = relations.progress_apply(add_relation, axis=1, g=g, ns=gn)

    # Store graph to turtle
    logging.info("Saving graph to turtle")
    g.serialize(path.join(base_dir, "geonames.ttl"), format="turtle")

    # Store processed dataframes for later use
    # logging.info("Saving processed data to csv")
    # countries.to_csv(path.join(base_dir, "allCountries_processed.csv"))
    # relations.to_csv(path.join(base_dir, "hierarchy_processed.csv"), index=False)
