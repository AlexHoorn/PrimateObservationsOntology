import re
from typing import Optional
import logging

import geocoder
from geocoder.geonames import GeonamesQuery
from rdflib import ConjunctiveGraph
from rdflib.plugins.sparql.processor import SPARQLResult

logger = logging.getLogger(__name__)

# NOTE: The stuff here has actually become irrelevant, so don't use it :)

def get(location: str) -> GeonamesQuery:
    return geocoder.geonames(location)


def get_parent_structure(geonames_id: int, graph: Optional[ConjunctiveGraph] = None):
    if not graph:
        graph = ConjunctiveGraph()

    # We query with an empty graph to prevent getting existing results
    empty_graph = ConjunctiveGraph()

    # The fetching queue
    todo = set([geonames_id])

    while todo:
        geo_id: int = todo.pop()

        try:
            result: SPARQLResult = empty_graph.query(
                """
                select * 
                from <http://sws.geonames.org/%i/about.rdf>
                where { ?s ?p ?o }
                """
                % geo_id
            )

            for row in result:
                # Ordering might be wrong if you do; for s,p,o in result
                s, p, o = row.s, row.p, row.o

                # Add relation to parent
                if "#parent" in p:
                    graph.add((s, p, o))
                    parent_id: str = re.findall("[0-9]+", o)[0]

                    # Add parent to queue if it's not in the graph yet
                    if parent_id not in graph.subjects():
                        todo.add(int(parent_id))

                # Add the official name to the graph
                # TODO: the rdf has language codes, but it's not shown here?
                if "#officialName" in p:
                    graph.add((s, p, o))
        except Exception as e:
            logger.warning(e)

    return graph
