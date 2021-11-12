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
	path='https://raw.githubusercontent.com/Julia-upc/Curso2021-2022-ODKG/master/HandsOn/Group10'
	g = Graph()
	g.namespace_manager.bind('default', Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#"),override=False)
	g.parse(path+'/rdf/RDF-with-links.ttl', format="turtle")
	default=Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#")
	q = prepareQuery('''
	SELECT ?title ?startDate ?endDate ?location  ?price ?link WHERE { 
	?event a default:Event.
	?event default:title ?title.
	?event default:startDate ?startDate.
	?event default:takesPlaceIn ?location.
	?event default:endDate ?endDate.
	?event default:price ?price.
	?event default:URI ?link
	}
	''',
	initNs = { "default": default} 
	)

	queryOut = g.query(q)
	datos=[]
	
	for event, startDate, location, endDate, price, link in queryOut:
		datos.append([str(event), str(startDate), str(endDate), str(location), str(price), str(link)])

	return(datos)








	
