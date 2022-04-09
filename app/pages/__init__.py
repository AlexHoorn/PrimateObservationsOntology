from typing import Callable, Dict
from .map_all import page_map_all
from .query_test import page_query_test

pages: Dict[str, Callable] = {
    "All observations": page_map_all,
    "Query test": page_query_test,
}
