import csv
from rdflib import Graph, Literal, Namespace, URIRef
import pandas as pd
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD


input_file = "primate.txt"


# make a graph
output_graph = Graph()
EX = Namespace("https://example.org/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/TR/2004/REC-owl-guide-20040210/")

def convert_str(line):
	line = line.strip('\n')
	rank = line.split(' ')[-1].strip('[]')

	space_number, synonym = count_space(line)
	if synonym:
		class_name = line[space_number+1:-len(rank) - 2]
	else:
		class_name = line[space_number:-len(rank) - 2]
	if "(" and ")" in class_name:
		name = class_name.split("(")[0]
		author = class_name.split("(")[-1][:-2].split(",")[0]
		year = int(class_name.split("(")[-1][:-2].split(",")[-1].strip(' '))
	else:
		name = class_name.split(",")[0]
		year = class_name.split(",")[-1]
		author = None
	detail_info = {"rank":rank,"class_name":class_name,"space_number":space_number,"synonym":synonym,
				   "name":name,"author":author,"year":year}

	return detail_info

def count_space(line):
	count = 0
	synonym = 0
	for i in line:
		if i==" ":
			count += 1
		elif i == '*':
			synonym = 1
			break
		else:
			break
	return count, synonym

fathers = {}

with open(input_file,'r') as f:
	line_former = {}
	result = []
	detail_info_former={}
	for line in f.readlines():
		detail_info = convert_str(line)

		name = detail_info.get("name", '')
		synonym = detail_info['synonym']
		space_number = detail_info['space_number']
		rank = detail_info['rank']
		fathers[space_number//2]=detail_info['name']

		if synonym == 1:
			father = detail_info_former.get('father', '')

		elif space_number > detail_info_former.get('space_number', 0):
			father = detail_info_former.get('name', '')
		elif space_number == line_former.get('space_number', 0):
			father = detail_info_former.get('father', '')
		else:
			father = fathers.get(space_number//2 - 1,0)

		# rdf

		if synonym == 1:
			output_graph.add(
			(EX + URIRef(name), owl + URIRef('equivalentClass'), EX + URIRef(detail_info_former.get('name', ''))))
		else:
			output_graph.add(
				(EX + URIRef(name), rdfs + URIRef('subclassOf'), EX + URIRef(detail_info_former.get('name', ''))))

		# store_father_info
		detail_info['father'] = father
		detail_info_former = detail_info
	# 	result.append(detail_info)
	# df=pd.DataFrame(result)
	# df.to_csv('result.csv')
output_graph.serialize(destination='taxanomy.rdf', format='xml')



	#{'Subject Label': 'Pearl Wilmer Booker', 'Subject EX+URI': 'None', 'Predicate Label': 'Daughter Of', 'Predicate EX+URI': '', 'Predicate Symmetry': 'Asymmetric', 'Object Label': 'Mary Booker', 'Object EX+URI': 'None'}
	# make a literal and add it
	# subject = row['Painter']
	# object = row['Painting']
	# output_graph.add((EX+URIRef(subject), EX+URIRef('authorOf'), EX+URIRef(object)))
	# output_graph.add((EX+URIRef(row['Painting']), EX+URIRef('paintby'), EX+URIRef(row['Painter'])))
	# output_graph.add((EX+URIRef(row['Painting']), EX+URIRef('storedin'), EX+URIRef(row['Museum'])))
	# output_graph.add((EX+URIRef(row['Painter']), EX+URIRef('hasMovement'), EX+URIRef(row['Movement'])))
	# output_graph.add((EX+URIRef(row['Museum']), EX+URIRef('locatedIn'), EX+URIRef(row['Location'])))
	# output_graph.add((EX+URIRef(row['Painter']), EX+URIRef('birthAt'), EX+URIRef(row['Birthplace'])) )
	# output_graph.add((EX+URIRef(row['Painter']), EX+URIRef('birthOn'), EX+URIRef(row['Birthdate'])) )
	# output_graph.add((EX + URIRef(row['Country']), EX + URIRef('contains'), EX+URIRef(row['Location'])))
	#
	# output_graph.add((EX+URIRef(row['Painter']), rdf.type,EX+URIRef('Painter') ))
	# output_graph.add((EX+URIRef(row['Painting']), rdf.type,EX+URIRef('Painting') ))
	# output_graph.add((EX+URIRef(row['Museum']), rdf.type,EX+URIRef('Museum') ))
	# output_graph.add((EX+URIRef(row['Location']), rdf.type,EX+URIRef('City') ))
	# output_graph.add((EX+URIRef(row['Movement']), rdf.type,EX+URIRef('Movement') ))
	# output_graph.add((EX+URIRef(row['Birthplace']), rdf.type,EX+URIRef('Birthplace') ))






# output_graph.serialize(destination='taxanomy.rdf', format='xml')




