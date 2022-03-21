import logging
from os import path

import pandas as pd
from rdflib import RDF, ConjunctiveGraph, Literal, Namespace
from tqdm import tqdm

base_dir = path.dirname(__file__)
observations_file = path.join(
    base_dir, "observation_data", "inaturalist", "observations_mapped.csv"
)

logging.basicConfig(
    format="%(asctime)s %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
)

# Function to add triple to graph from dataframe row
def add_observation(row: pd.Series, g: ConjunctiveGraph, ns: Namespace, gn: Namespace):
    s = getattr(ns, str(row.name))

    g.add((s, RDF.type, ns.Observation))
    g.add((s, ns.observedOn, Literal(row["observed_on"])))
    g.add((s, ns.url, Literal(row["url"])))
    g.add((s, ns.captiveCultivated, Literal(row["captive_cultivated"])))
    g.add((s, ns.latitude, Literal(row["latitude"])))
    g.add((s, ns.longitude, Literal(row["longitude"])))
    g.add((s, ns.taxonId, Literal(row["taxon_id"])))

    geo = getattr(gn, str(row["geonameid"]))
    g.add((s, ns.locatedAt, geo))


if __name__ == "__main__":
    # Load observations
    logging.info("Loading observations dataframe")
    observations = pd.read_csv(
        observations_file,
        parse_dates=["observed_on", "time_observed_at"],
    )

    # Create the graph to collect everything
    logging.info("Loading geonames graph, might take a while")
    g = ConjunctiveGraph()
    g.parse(path.join(base_dir, "geonames", "geonames.ttl"))

    # Namespaces
    inat = Namespace("http://www.inaturalist.org/ontology#")
    g.namespace_manager.bind("inat", inat)
    gn = Namespace(dict(g.namespace_manager.namespaces())["gn"])

    # Add observations from dataframe
    tqdm.pandas(desc="Adding observations")
    _ = observations.progress_apply(add_observation, axis=1, g=g, ns=inat, gn=gn)

    # Store graph to turtle
    logging.info("Saving graph to turtle")
    g.serialize(path.join(base_dir, "observations.ttl"), format="ttl")

    # NOTE: This is unfinished
    # For example, it does not contain the hierarchy of species, genus, etc.
