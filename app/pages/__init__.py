from typing import Callable, Dict

from .distribution_obs import distribution_obs
from .homepage import page_home
from .query_test import page_query_test
from .sparql_endpoint import sparql_endpoint
from .observations_count import page_observations_count
from .observations_trend import page_observations_trend

pages: Dict[str, Callable] = {
    "🏠 Homepage": page_home,
    "📊 Observation counts": page_observations_count,
    "Distribution of Observations": distribution_obs,
    "Trend of observations": page_observations_trend,
    "🧪 Query test": page_query_test,
    "🔬 Sparql Endpoint": sparql_endpoint,
}
