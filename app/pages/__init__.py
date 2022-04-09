from typing import Callable, Dict
from .map_all import page_map_all
from .query_test import page_query_test
from .sparql_endpoint import sparql_endpoint
from .distribution_obs import distribution_obs

pages: Dict[str, Callable] = {
    "All observations": page_map_all,
    "Query test": page_query_test,
    "Sparql Endpoint": sparql_endpoint,
    "Distribution of Observations": distribution_obs
}
