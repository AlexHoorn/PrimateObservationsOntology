import logging
import os

os.environ["GEONAMES_USERNAME"] = "alexhn"

# To surpress all the rdflib serialization warnings
logger = logging.getLogger("rdflib")
logger.setLevel(logging.ERROR)
