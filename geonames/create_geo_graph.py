# %% Packages
import logging

import pandas as pd
from rdflib import RDFS, ConjunctiveGraph, Literal, Namespace
from tqdm import tqdm

logging.basicConfig(
    format="%(asctime)s %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
)

# %% Function to add a relation from a pandas series
def add_relation(row: pd.Series, g: ConjunctiveGraph, ns: Namespace) -> None:
    s = getattr(ns, str(row.childId))
    o = getattr(ns, str(row.parentId))

    g.add((s, ns.partOf, o))


# %% Load dataframe of all geonames entities (~12mil rows)
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

logging.info("Loading allCountries dataframe")
countries = pd.read_csv(
    "allCountries.txt", sep="\t", names=all_countries_cols, index_col=0
)
countries.head()

# %% Load dataframe of all geonames hierarchy relations
logging.info("Loading relations dataframe")
relations = pd.read_csv(
    "hierarchy.txt", sep="\t", names=["parentId", "childId", "type"]
)
relations.head()

# %% Create new empty graph
logging.info("Setting up new graph")
g = ConjunctiveGraph()
gn = Namespace("http://www.geonames.org/ontology#")

g.namespace_manager.bind("gn", gn)

# %% Add entity information to graph
for geo_id in tqdm(
    # NOTE: Currently only entities with relations are added
    set(relations.parentId) | set(relations.childId),
    desc="Adding general subject information",
):
    try:
        row = countries.loc[geo_id]
        s = getattr(gn, str(geo_id))

        g.add((s, RDFS.label, Literal(row["name"])))
        g.add((s, gn.countryCode, Literal(row["country code"])))
        g.add((s, gn.latitude, Literal(row["latitude"])))
        g.add((s, gn.longitude, Literal(row["longitude"])))
        g.add((s, gn.featureClass, Literal(row["feature class"])))
        g.add((s, gn.featureCode, Literal(row["feature code"])))

    except KeyError:
        pass

# %% Add hierarchical relations
tqdm.pandas(desc="Adding partOf relations")
_ = relations.progress_apply(add_relation, axis=1, g=g, ns=gn)

# %% Store graph to xml/turtle
logging.info("Saving graph to xml")
g.serialize("geonames.xml", format="xml")
logging.info("Saving graph to turtle")
g.serialize("geonames.ttl", format="turtle")
