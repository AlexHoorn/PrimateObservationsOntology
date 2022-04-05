First, import the taxslim.owl ontology into GraphDB, and put it in the named graph <http://ex.org/graph1>

Then, get the observations CSV, import it into OntoRefine, and import the JSON mapping called OntoRefine_mapping. 

Then, export that merge to rdf, and reimport it as RDF in GraphDB under the named graph <http://ex.org/triples_full>

Finally, run the SPARQL query and export the merged_graph. You can visualize it in Protege to get a better idea of its structure.