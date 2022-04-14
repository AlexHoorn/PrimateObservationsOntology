from typing import Callable, Dict

from .homepage import page_home
from .observations_dist import page_observations_dist
from .observations_map import page_observations_count
from .observations_trend import page_observations_trend
from .sparql_endpoint import page_sparql_endpoint

pages: Dict[str, Callable] = {
    "🏠 Homepage": page_home,
    "🌍 Observations Map": page_observations_count,
    "🔃 Observations Spread": page_observations_dist,
    "📈 Observations Trend": page_observations_trend,
    "🧪 Sparql Endpoint": page_sparql_endpoint,
}
