
# Info
the basic taxonomy ontology is the  NCBI taxonomy classification, converted to RDF.
The taxonomic class ID equivalencies are extracted from Wikidata. Wikidata keeps a reference of equivalent class ID's across naming authorities. for example, NCBI ID 9606 = ITIS ID 180092).
Naming authorities considered here are Encyclopedia of Life (EOL), iNaturalist, ITIS and GBIF.
The actual instances are extracted from iNaturalist, and are mapped to the right NCBI taxon via their NCBI Taxon ID. 

# WebApp Installation and Execution :

1. Make sure GraphDB (or any similar Knowledge Graph hosting server) is installed and running properly on your system.
2. Import our complete ontology from the directory root/ontology, with the name "primate_taxonomy.ttl" into your active GraphDB repository.
3. Change "sparql_endpoint : sparql_endpoint_address" in app/config.yaml to "sparql_endpoint : YOUR_LOCAL_SPARQL_REPO_ADDRESS". In GraphDB, this address can be found in Setup->Repositories tab. 
4. Install the required python dependences in your python installation/virtual environment using app/requirements.txt.
Example Syntax : pip install -r requirements.txt
5. Voila! Run the app from the terminal using "streamlit run app.py" in the app directory.

# Instructions for Recreating our ontology :

First, import the taxslim.owl ontology into GraphDB (lightweight version of the NCBI taxonomy) into the named graph <http://ex.org/graph1>

Optionally, get the observations CSV, import it into OntoRefine, and import the JSON mapping called OntoRefine_mapping. Export as RDF. 
Reimport it as RDF in GraphDB under the named graph <http://ex.org/triples_full>. 

Alternatively, you can also directly import the pre-existing RDF file called observations_from_csv.ttl.

Then, import the wikidata_rdf.ttl file into <http://ex.org/wikidata>. 


Finally, run the SPARQL query and export the merged_graph. You can visualize it in Protege to get a better idea of its structure.
