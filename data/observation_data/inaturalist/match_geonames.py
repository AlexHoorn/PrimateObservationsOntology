import logging
from functools import partial
from multiprocessing import Pool
from os import path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
from tqdm import tqdm

logging.basicConfig(
    format="%(asctime)s %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
)

# Function that returns closest geonameid
def closest_geoname(
    latlon: np.ndarray, c_ids: np.ndarray, c_latlons: np.ndarray
) -> np.int_:
    closest_idx = haversine_distances(c_latlons, np.array([latlon])).argmin()
    return c_ids[closest_idx]


# We do this construction because the mapping is multithreaded
if __name__ == "__main__":
    base_dir = path.dirname(__file__)

    # Load observations
    logging.info("Reading observations")
    observations = pd.read_csv(
        (path.join(base_dir, "observations-216923.csv")), index_col=0
    )

    # Load geonames info
    logging.info("Reading countries")
    countries = pd.read_csv(
        path.join(base_dir, "../../geonames/allCountries_processed.csv"),
        index_col=0,
        usecols=["geonameid", "latitude", "longitude"],
    )

    c_latlons = countries[["latitude", "longitude"]].values
    c_ids = countries.index.values

    logging.info("Executing mapping")
    # Create the function to run everything with
    p_closest_geoname = partial(closest_geoname, c_ids=c_ids, c_latlons=c_latlons)

    # Start multithreading
    with Pool() as pool:
        # Make a list of tasks we'll perform
        futures = pool.imap(
            p_closest_geoname,
            observations[["latitude", "longitude"]].values,
        )
        # Get a list of the results of the tasks
        results = list(tqdm(futures, total=len(observations)))

    # Add results as a column
    observations["geonameid"] = results

    observations.to_csv(path.join(base_dir, "observations_mapped.csv"))
