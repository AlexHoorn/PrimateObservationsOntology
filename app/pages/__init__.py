from typing import Callable, Dict

from .homepage import page_home
from .observations_dist import page_observations_dist
from .observations_map import page_observations_count
from .observations_trend import page_observations_trend
from .sparql_endpoint import page_sparql_endpoint

pages: Dict[str, Callable] = {
    "๐  Homepage": page_home,
    "๐ Observations Map": page_observations_count,
    "๐ Observations Spread": page_observations_dist,
    "๐ Observations Trend": page_observations_trend,
    "๐งช Sparql Endpoint": page_sparql_endpoint,
}
