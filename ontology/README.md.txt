
# INFO
the basic taxonomy ontology is the  NCBI taxonomy classification, converted to RDF.
The taxonomic class ID equivalencies are extracted from Wikidata. Wikidata keeps a reference of equivalent class ID's across naming authorities. (for example, NCBI id 9505 = ITIS id 2345)
Naming authorities considered here are Encyclopedia of Life (EOL), iNaturalist, ITIS and GBIF.
The actual instances are extracted from iNaturalist, and are mapped to the right NCBI taxon via their NCBI Taxon ID. 

# instructions 

First, import the taxslim.owl ontology into GraphDB (lightweight version of the NCBI taxonomy) into the named graph <http://ex.org/graph1>

Optionally, get the observations CSV, import it into OntoRefine, and import the JSON mapping called OntoRefine_mapping. Export as RDF. 
Reimport it as RDF in GraphDB under the named graph <http://ex.org/triples_full>. 

Alternatively, you can also directly import the pre-existing RDF file called observations_from_csv.ttl.

Then, import the wikidata_rdf.ttl file into <http://ex.org/wikidata>. 


Finally, run the SPARQL query and export the merged_graph. You can visualize it in Protege to get a better idea of its structure.