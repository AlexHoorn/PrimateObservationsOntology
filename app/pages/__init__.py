from typing import Callable, Dict
from .homepage import page_home
from .query_test import page_query_test
from .sparql_endpoint import sparql_endpoint
from .observations_count import page_observations_count

pages: Dict[str, Callable] = {
    "🏠 Homepage": page_home,
    "📊 Observation counts": page_observations_count,
    "🧪 Query test": page_query_test,
    "🔬 Sparql Endpoint": sparql_endpoint,
}
