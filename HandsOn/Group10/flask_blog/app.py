from flask import Flask, render_template
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, FOAF
from rdflib.plugins.sparql import prepareQuery

import sys

app = Flask(__name__)

@app.route('/madridEvents')
def index():
    query()
    return render_template('index.html')
	

def query():
	path='https://raw.githubusercontent.com/Julia-upc/Curso2021-2022-ODKG/master/HandsOn/Group10'
	g = Graph()
	g.namespace_manager.bind('default', Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#"),override=False)		
	g.parse(path+'/rdf/RDF-with-links.ttl', format="turtle")
	default=Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#")

	q1 = prepareQuery('SELECT ?x WHERE { ?x a default:Facility.  ?x default:accessible "true" }',initNs = { "default": default})
	for r in g.query(q1):
		print(r, file=sys.stderr)

	print(len(g.query(q1)), file=sys.stderr)
	
