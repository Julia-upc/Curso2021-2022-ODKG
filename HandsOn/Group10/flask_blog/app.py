from flask import Flask, render_template
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, FOAF
from rdflib.plugins.sparql import prepareQuery
from flask import request



app = Flask(__name__)

@app.route('/madridEvents', )

def index():
	headers = ['Event Title','Init Date','End Date','Location','Price','Link']
	table = query_inicial()
	if request.method == 'POST':
		return "<p>Hello, World!</p>"
	else:
		return render_template('index.html',headers=headers, objects=table)
	



def query_inicial():
	RDFsource = "https://raw.githubusercontent.com/pablo-crucera/Curso2021-2022-ODKG/master/HandsOn/eventosfinal-deverdad.ttl"
	from rdflib import Graph, Namespace, Literal
	from rdflib.namespace import RDF, RDFS
	from rdflib.plugins.sparql import prepareQuery

	g = Graph()
	g.namespace_manager.bind('ns', Namespace("http://www.example.org#"), override=False)
	g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
	g.namespace_manager.bind('xsd', Namespace("http://www.w3.org/2001/XMLSchema#"), override=False)
	g.namespace_manager.bind('smart', Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#"), override=False)
	g.parse(RDFsource, format="ttl")

	smart = Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#")
	xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
	q = prepareQuery('''
		SELECT ?title ?startDate ?endDate ?location ?price ?link WHERE { 
		?event a smart:Event.
		?event smart:title ?title.
		?event smart:startDate ?startDate.
		?event smart:takesPlaceIn ?facility.
		?facility smart:name ?location.
		?event smart:endDate ?endDate.
		?event smart:price ?price.
		?event smart:URI ?link
		}
		''',
		initNs = { "smart": smart, "xsd": xsd} 
	)
	
	queryOut = g.query(q)
	return queryOut
	








	
