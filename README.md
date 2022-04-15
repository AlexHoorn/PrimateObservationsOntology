
# Info
the basic taxonomy ontology is the  NCBI taxonomy classification, converted to RDF.
The taxonomic class ID equivalencies are extracted from Wikidata. Wikidata keeps a reference of equivalent class ID's across naming authorities (for example, NCBI ID 9606 = ITIS ID 180092).
Naming authorities considered here are Encyclopedia of Life (EOL), iNaturalist, ITIS and GBIF.
The actual instances are extracted from iNaturalist, and are mapped to the right NCBI taxon via their NCBI Taxon ID. 

# WebApp Installation and Execution :
Method 1:

1.clone the repository and install the requirements.
2. Make sure GraphDB (or any similar Knowledge Graph hosting server) is installed and running properly on your system.

3. Import our complete ontology from the directory root/ontology, with the name "primate_taxonomy.ttl" into your active GraphDB repository.

4. Change "sparql_endpoint : sparql_endpoint_address" in app/config.yaml to "sparql_endpoint : YOUR_LOCAL_SPARQL_REPO_ADDRESS". In GraphDB, this address can be found in Setup->Repositories tab. 
5. Install the required python dependences in your python installation/virtual environment using app/requirements.txt.

Example Syntax : pip install -r requirements.txt

6. Voila! Run the app from the terminal using "streamlit run app.py" in the app directory.

Method 2(use Docker):

1. install docker and initialize docker.
2. clone this repository.(if app's load speed is too low,you can also use graphDB and change
"sparql_endpoint_address" in app/config.yaml )
3. build image (there is . in the end of this command)
```shell script
docker build -t streamlitapp:latest . 
```
4. run code
```shell script
docker run -p 8501:8501 streamlitapp:latest
```



# Instructions for Recreating our ontology :

First, import the taxslim.owl ontology into GraphDB (lightweight version of the NCBI taxonomy) into the named graph <http://ex.org/graph1>

Optionally, get the observations CSV, import it into OntoRefine, and import the JSON mapping called OntoRefine_mapping. Export as RDF. 
Reimport it as RDF in GraphDB under the named graph <http://ex.org/triples_full>. 

Alternatively, you can also directly import the pre-existing RDF file called observations_from_csv.ttl.

Then, import the wikidata_rdf.ttl file into <http://ex.org/wikidata>. 


Finally, run the SPARQL query and export the merged_graph. You can visualize it in Protege to get a better idea of its structure.

# Ontology documentation

Metadata
--------

**IRI**

`https://krr.triply.cc/NathanV/KRWprimatestaxonomy/graphs/default`

[Title](http://purl.org/dc/terms/title "A name given to the resource. Defined in DCMI Metadata Terms")

Primate Taxonomy Ontology

[Creator](http://purl.org/dc/terms/creator "An entity responsible for making the resource. Defined in DCMI Metadata Terms")

*   Alex Hoorn
    
*   Bram Kreuger
    
*   Nathan Vaartjes
    
*   Sunny Soni
    
*   Yuyu Bai
    

[Date Created](http://purl.org/dc/terms/created "Date of creation of the resource. Defined in DCMI Metadata Terms")

0101-01-01

[Description](http://purl.org/dc/terms/description "An account of the resource. Defined in DCMI Metadata Terms")

This ontolgy combines the taxonomic classes of the NCBI taxonomy (http://purl.obolibrary.org/obo/ncbitaxon.owl) and populates it with observations from iNaturalist (https://www.inaturalist.org/). Every observations has a location ID, latitude longitude, and is mapped to the right NCBI taxon (class) via its NCBI taxon ID.

Example classes
---------------

### Homo c

IRI

`http://purl.obolibrary.org/obo/NCBITaxon_9605`

[Sub Class Of](http://www.w3.org/2000/01/rdf-schema#subClassOf "The subject is a subclass of a class. Defined in The RDF Schema vocabulary (RDFS)")

[ncbi:207598](http://purl.obolibrary.org/obo/NCBITaxon_207598) c

[Super Class Of](https://w3id.org/profile/ontdoc/superClassOf "Inverse of RDFS' subClassOf. Defined in Ontology Documentation Profile")

[ncbi:9606](http://purl.obolibrary.org/obo/NCBITaxon_9606) c

### Homo sapiens c

IRI

`http://purl.obolibrary.org/obo/NCBITaxon_9606`

[Sub Class Of](http://www.w3.org/2000/01/rdf-schema#subClassOf "The subject is a subclass of a class. Defined in The RDF Schema vocabulary (RDFS)")

[ncbi:9605](http://purl.obolibrary.org/obo/NCBITaxon_9605) c

### Gorilla gorilla gorilla c

IRI

`http://purl.obolibrary.org/obo/NCBITaxon_9595`

[Sub Class Of](http://www.w3.org/2000/01/rdf-schema#subClassOf "The subject is a subclass of a class. Defined in The RDF Schema vocabulary (RDFS)")

[ncbi:9593](http://purl.obolibrary.org/obo/NCBITaxon_9593) c

### family c

IRI

`http://purl.obolibrary.org/obo/NCBITaxon_family`

[Sub Class Of](http://www.w3.org/2000/01/rdf-schema#subClassOf "The subject is a subclass of a class. Defined in The RDF Schema vocabulary (RDFS)")

[ns2:\_taxonomic\_rank](http://purl.obolibrary.org/obo/NCBITaxon#_taxonomic_rank) c

### taxonomic rank c

IRI

`http://purl.obolibrary.org/obo/NCBITaxon#_taxonomic_rank`

[Description](http://purl.org/dc/terms/description "An account of the resource. Defined in DCMI Metadata Terms")

This is an abstract class for use with the NCBI taxonomy to name the depth of the node within the tree. The link between the node term and the rank is only visible if you are using an obo 1.3 aware browser/editor; otherwise this can be ignored.

[Super Class Of](https://w3id.org/profile/ontdoc/superClassOf "Inverse of RDFS' subClassOf. Defined in Ontology Documentation Profile")

*   [ncbi:class](http://purl.obolibrary.org/obo/NCBITaxon_class) c
*   [ncbi:family](http://purl.obolibrary.org/obo/NCBITaxon_family) c
*   [ncbi:genus](http://purl.obolibrary.org/obo/NCBITaxon_genus) c
*   [ncbi:infraclass](http://purl.obolibrary.org/obo/NCBITaxon_infraclass) c
*   [ncbi:infraorder](http://purl.obolibrary.org/obo/NCBITaxon_infraorder) c
*   [ncbi:kingdom](http://purl.obolibrary.org/obo/NCBITaxon_kingdom) c
*   [ncbi:order](http://purl.obolibrary.org/obo/NCBITaxon_order) c
*   [ncbi:parvorder](http://purl.obolibrary.org/obo/NCBITaxon_parvorder) c
*   [ncbi:phylum](http://purl.obolibrary.org/obo/NCBITaxon_phylum) c
*   [ncbi:species](http://purl.obolibrary.org/obo/NCBITaxon_species) c
*   [ncbi:subclass](http://purl.obolibrary.org/obo/NCBITaxon_subclass) c
*   [ncbi:subfamily](http://purl.obolibrary.org/obo/NCBITaxon_subfamily) c
*   [ncbi:subgenus](http://purl.obolibrary.org/obo/NCBITaxon_subgenus) c
*   [ncbi:suborder](http://purl.obolibrary.org/obo/NCBITaxon_suborder) c
*   [ncbi:subphylum](http://purl.obolibrary.org/obo/NCBITaxon_subphylum) c
*   [ncbi:subspecies](http://purl.obolibrary.org/obo/NCBITaxon_subspecies) c
*   [ncbi:subtribe](http://purl.obolibrary.org/obo/NCBITaxon_subtribe) c
*   [ncbi:superclass](http://purl.obolibrary.org/obo/NCBITaxon_superclass) c
*   [ncbi:superfamily](http://purl.obolibrary.org/obo/NCBITaxon_superfamily) c
*   [ncbi:superkingdom](http://purl.obolibrary.org/obo/NCBITaxon_superkingdom) c
*   [ncbi:superorder](http://purl.obolibrary.org/obo/NCBITaxon_superorder) c
*   [ncbi:superphylum](http://purl.obolibrary.org/obo/NCBITaxon_superphylum) c
*   [ncbi:tribe](http://purl.obolibrary.org/obo/NCBITaxon_tribe) c
*   [ncbi:varietas](http://purl.obolibrary.org/obo/NCBITaxon_varietas) c
*   [ns2:\_species\_group](http://purl.obolibrary.org/obo/NCBITaxon#_species_group) c
*   [ns2:\_species\_subgroup](http://purl.obolibrary.org/obo/NCBITaxon#_species_subgroup) c

### Location c

IRI

`http://purl.org/dc/terms/Location`

### Occurrence c

IRI

`http://rs.tdwg.org/dwc/terms/Occurrence`

[Description](http://purl.org/dc/terms/description "An account of the resource. Defined in DCMI Metadata Terms")

Class used to denote observations populating the ontology

Annotation Properties
---------------------

### common name ap

IRI

`http://purl.obolibrary.org/obo/ncbitaxon#common_name`

[Sub Property Of](http://www.w3.org/2000/01/rdf-schema#subPropertyOf "The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)")

[oboInOwl:SynonymTypeProperty](http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty) ap

### equivalent name ap

IRI

`http://purl.obolibrary.org/obo/ncbitaxon#equivalent_name`

[Sub Property Of](http://www.w3.org/2000/01/rdf-schema#subPropertyOf "The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)")

[oboInOwl:SynonymTypeProperty](http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty) ap

### has\_rank ap

IRI

`http://purl.obolibrary.org/obo/ncbitaxon#has_rank`

### scientific name ap

IRI

`http://purl.obolibrary.org/obo/ncbitaxon#scientific_name`

[Sub Property Of](http://www.w3.org/2000/01/rdf-schema#subPropertyOf "The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)")

[oboInOwl:SynonymTypeProperty](http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty) ap

### synonym ap

IRI

`http://purl.obolibrary.org/obo/ncbitaxon#synonym`

[Sub Property Of](http://www.w3.org/2000/01/rdf-schema#subPropertyOf "The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)")

[oboInOwl:SynonymTypeProperty](http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty) ap

### teleomorph ap

IRI

`http://purl.obolibrary.org/obo/ncbitaxon#teleomorph`

[Sub Property Of](http://www.w3.org/2000/01/rdf-schema#subPropertyOf "The subject is a subproperty of a property. Defined in The RDF Schema vocabulary (RDFS)")

[oboInOwl:SynonymTypeProperty](http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty) ap

Namespaces
----------

dc

`http://purl.org/dc/elements/1.1/`

dcterms

`http://purl.org/dc/terms/`

dwc

`http://rs.tdwg.org/dwc/terms/`

gbif

`https://www.gbif.org/species/`

inat

`https://www.inaturalist.org/`

inat\_taxa

`https://www.inaturalist.org/taxa/`

itis

`https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=`

ncbi

`http://purl.obolibrary.org/obo/NCBITaxon_`

ncbitaxon

`http://purl.obolibrary.org/obo/ncbitaxon#`

ns1

`https://krr.triply.cc/NathanV/KRWprimatestaxonomy/graphs/`

ns2

`http://purl.obolibrary.org/obo/NCBITaxon#`

obo

`http://purl.obolibrary.org/obo/`

oboInOwl

`http://www.geneontology.org/formats/oboInOwl#`

owl

`http://www.w3.org/2002/07/owl#`

prov

`http://www.w3.org/ns/prov#`

rdf

`http://www.w3.org/1999/02/22-rdf-syntax-ns#`

rdfs

`http://www.w3.org/2000/01/rdf-schema#`

skos

`http://www.w3.org/2004/02/skos/core#`

xsd

`http://www.w3.org/2001/XMLSchema#`

Legend
------

c

Classes

ap

Annotation Properties

made by [p y LODE](https://github.com/rdflib/pyLODE) [3.0.2a](https://github.com/rdflib/pyLODE/release/3.0.2a)

### Table of Contents

*   #### [Metadata](#metadata)
    
*   #### [Classes](#classes)
    
    *   [Homo](#Homo)
    *   [Gorilla gorilla gorilla](#gorillagorillagorilla)
    *   [Homo Sapiens](#Homo Sapiens)
    *   [family](#family)
    *   [taxonomic rank](#taxonomicrank)
    *   [Location](#Location)
    *   [Occurrence](#Occurrence)
*   #### [Annotation Properties](#annotationproperties)
    
    *   [common name](#commonname)
    *   [equivalent name](#equivalentname)
    *   [has\_rank](#has_rank)
    *   [scientific name](#scientificname)
    *   [synonym](#synonym)
    *   [teleomorph](#teleomorph)
*   #### [Namespaces](#namespaces)
    
    *   [dc](#dc)
    *   [dcterms](#dcterms)
    *   [dwc](#dwc)
    *   [gbif](#gbif)
    *   [inat](#inat)
    *   [inat\_taxa](#inat_taxa)
    *   [itis](#itis)
    *   [ncbi](#ncbi)
    *   [ncbitaxon](#ncbitaxon)
    *   [ns1](#ns1)
    *   [ns2](#ns2)
    *   [obo](#obo)
    *   [oboInOwl](#oboInOwl)
    *   [owl](#owl)
    *   [prov](#prov)
    *   [rdf](#rdf)
    *   [rdfs](#rdfs)
    *   [skos](#skos)
    *   [xsd](#xsd)
*   #### [Legend](#legend)
