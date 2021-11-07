from flask import Flask, render_template
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, FOAF
from rdflib.plugins.sparql import prepareQuery

import sys

app = Flask(__name__)

@app.route('/madridEvents')
def index():
    return render_template('index.html')
	



def query_inicial():
	q = prepareQuery('''
	#  SELECT ?title ?startDate ?locationName ?endDate ?price ?link WHERE{
	  SELECT ?title ?startDate ?location ?endDate ?price ?link WHERE { #
	    ?event a default:Event.
	    ?event default:title ?title.
	    ?event default:startDate ?startDate.
	    ?event default:takesPlaceIn ?location.
	#    ?event default:locationName ?locationName.
	    ?event default:endDate ?endDate.
	    ?event default:price ?price.
	    ?event default:URI ?link
	  } LIMIT 50
	  ''',
	  initNs = { "default": default, "xsd": xsd} 
	)

	queryOut = g.query(q)
	print("Event", "Start Date", "Location", "End Date", "Price", "Link")
	for event, startDate, location, endDate, price, link in queryOut:
	  print(event, startDate, location, endDate, price, link)





def filtrograt(par):
	  events = []
	  if par == True:
	    for s1,p1,o1 in g.triples((None, RDF.type, default.Event)):
	      for s2,p2,o2 in g.triples((s1,default.free,Literal("true"))):
		for s3,p3,o3 in g.triples((s2, default.title,None)):
		  events.append(o3)
	  else:
	    for s1,p1,o1 in g.triples((None, RDF.type, default.Event)):
	      for s2,p2,o2 in g.triples((s1,default.free,Literal("false"))):
		for s3,p3,o3 in g.triples((s2, default.title,None)):
		  events.append(o3)
	  return events

	a = filtrograt(True)
	print(a)




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
	
