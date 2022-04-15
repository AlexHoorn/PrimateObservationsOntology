
# Info
The basic taxonomy ontology is the  NCBI taxonomy classification, converted to RDF.
The taxonomic class ID equivalencies are extracted from Wikidata. Wikidata keeps a reference of equivalent class ID's across naming authorities (for example, NCBI ID 9606 = ITIS ID 180092).
Naming authorities considered here are Encyclopedia of Life (EOL), iNaturalist, ITIS and GBIF.
The actual instances are extracted from iNaturalist, and are mapped to the right NCBI taxon via their NCBI Taxon ID. 

# WebApp Installation and Execution :

## Method 1 (without Docker):

1. Clone the repository.

2. (Optional, but recommended) Locally host the ontology
   1. Make sure GraphDB (or any similar Knowledge Graph hosting server) is installed and running properly on your system.
   2. Import our complete ontology `ontology/primate_taxonomy.ttl` into your active GraphDB repository.
   3. Change `sparql_endpoint : sparql_endpoint_address` in `app/config.yaml` to `sparql_endpoint : YOUR_LOCAL_SPARQL_REPO_ADDRESS`. In GraphDB, this address can be found in Setup -> Repositories tab.

3. Install the required python dependences in your python installation or virtual environment using `app/requirements.txt`. Using `pip install -r requirements.txt`

4. Run the app from the terminal using `streamlit run app.py` with the app directory open.

## Method 2 (using Docker):

1. Clone this repository.

2. (Optional, but recommended) Locally host the ontology
   1. Make sure GraphDB (or any similar Knowledge Graph hosting server) is installed and running properly on your system.
   2. Import our complete ontology `ontology/primate_taxonomy.ttl` into your active GraphDB repository.
   3. Change `sparql_endpoint : sparql_endpoint_address` in `app/config.yaml` to `sparql_endpoint : YOUR_LOCAL_SPARQL_REPO_ADDRESS`. In GraphDB, this address can be found in Setup -> Repositories tab.

3. Build the image `docker build -t streamlitapp:latest .` (note the . in the end of this command)

4. Run the image `docker run -p 8501:8501 streamlitapp:latest`

# Instructions for Recreating our ontology :

1. Import the taxslim.owl ontology into GraphDB (lightweight version of the NCBI taxonomy) into the named graph <http://ex.org/graph1>

2. Do **one** of the following

   1. (Option 1) Get the observations CSV, import it into OntoRefine, and import the JSON mapping called OntoRefine_mapping. Export as RDF. 
Reimport it as RDF in GraphDB under the named graph <http://ex.org/triples_full>. 
   1. (Option 2) Directly import the pre-existing RDF file called observations_from_csv.ttl.

3. Import the wikidata_rdf.ttl file into <http://ex.org/wikidata>. 

4. Run the SPARQL query and export the merged_graph. You can visualize it in Protege to get a better idea of its structure.
