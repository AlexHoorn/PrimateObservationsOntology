from typing import Callable, Dict

from .observations_dist import page_observations_dist
from .homepage import page_home
from .sparql_endpoint import page_sparql_endpoint
from .observations_map import page_observations_count
from .observations_trend import page_observations_trend

pages: Dict[str, Callable] = {
    "🏠 Homepage": page_home,
    "🌍 Observation Map": page_observations_count,
    "🔃 Observations Spread": page_observations_dist,
    "📈 Observations Trend": page_observations_trend,
    "🧪 Sparql Endpoint": page_sparql_endpoint,
}
