# %% We set the username for the geonames API before importing geocoder

import os

os.environ["GEONAMES_USERNAME"] = "alexhn"
import geocoder

# %% To do a search for something just give it a string, notice how Amsterdam is misspelled here
ams = geocoder.geonames("Amstrdam")

# %% Geonames correctly found Amsterdam
print(ams.address)

# %% This is all the information we retrieved
print(f"Retrieved info: {ams.geojson}")
print(f"Geonames ID: {ams.geonames_id}")  # importantly, we have the ID
print(
    f"Latitude: {ams.lat}, Longtitude: {ams.lng}"
)  # we can show something on a map with latlon

# %% To query with rdflib
from rdflib import ConjunctiveGraph

g = ConjunctiveGraph()

# %% Query Amsterdam
qams = g.query(
    """
    select * 
    from <http://sws.geonames.org/2759794/about.rdf>
    where { ?s ?p ?o }
    """
)

for row in qams:
    if "parent" in row.p or "child" in row.p:
        print(row.p.toPython(), row.o.toPython())

# %% Query its parent, Kingdom of the Netherlands
qned = g.query(
    """
    select * 
    from <http://sws.geonames.org/2750405/about.rdf>
    where { ?s ?p ?o }
    """
)

for row in qned:
    print(row.s.toPython(), row.p.toPython())

# %% This is all the stuff the Kingdom of the Netherlands contains
qned_contains = g.query(
    """
    select * 
    from <http://sws.geonames.org/2750405/contains.rdf>
    where { ?s ?p ?o }
    """
)

for row in qned_contains:
    print(row.s.toPython(), row.p.toPython(), row.o.toPython())
