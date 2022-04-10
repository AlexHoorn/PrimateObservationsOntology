from typing import Callable, Dict

from .observations_dist import page_observations_dist
from .homepage import page_home
from .sparql_endpoint import sparql_endpoint
from .observations_count import page_observations_count
from .observations_trend import page_observations_trend

pages: Dict[str, Callable] = {
    "🏠 Homepage": page_home,
    "📊 Observation counts": page_observations_count,
    "Distribution of Observations": page_observations_dist,
    "📈 Trend of observations": page_observations_trend,
    "🧪 Sparql Endpoint": sparql_endpoint,
}
