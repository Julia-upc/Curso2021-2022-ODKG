from flask import Flask, render_template
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, FOAF
from rdflib.plugins.sparql import prepareQuery
from flask import request
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery



app = Flask(__name__)

@app.route('/madridEvents',methods=["GET", "POST"] )

def index():

	headers = ['Event Title','Init Date','End Date','Location','Price','Link']
	table = 0
	if request.method == 'POST':
		req = request.form.get("init")
		req1 = request.form.get("fin")
		req2 = request.form.get("grat")
		req3 = request.form.get("local")
		if req == "" and req1 == "" and str(req2) == "None" and req3 == "Todas":
			pass
		elif req != "" and req1 == "" and str(req2) == "None" and req3 == "Todas":
			#SOLO SE INDICA FECHA INICIAL
			table = 2
		elif req == "" and req1 != "" and str(req2) == "None" and req3 == "Todas":
			#SOLO SE INDICA FECHA FINAL
			table = 3
		elif req == "" and req1 == "" and req2 != "None" and req3 == "Todas":
			#SOLO SE BUSCAN EVENTOS GRATUITOS
			table = buscarEventosGratuitos()
			return render_template('index.html',headers=headers, objects=table)

		elif req == "" and req1 == "" and str(req2) == "None" and req3 != "Todas":
			#SOLO SE BUSCA UN TIPO DE EVENTOS
			table = buscarTipoDeEvento(req3)
			return render_template('index.html',headers=headers, objects=table)
		elif req != "" and req1 != "" and req2 != "None" and req3 == "Todas":
			#SE INDICAN FECHA INI Y FECHA FIN
			table = 4
		elif req != "" and req1 == "" and req2 != "None" and req3 == "Todas":
			#SE INDICAN FECHA INI Y GRATUITO
			table = 5
		elif req != "" and req1 == "" and str(req2) == "None" and req3 != "Todas":
			#SE INDICAN FECHA INI Y EVENTOS
			table = 6
		elif req == "" and req1 != "" and req2 != "None" and req3 == "Todas":
			#SE INDICAN FECHA FIN Y GRATUITO
			table = 7
		elif req == "" and req1 != "" and str(req2) == "None" and req3 != "Todas":
			#SE INDICAN FECHA FIN Y EVENTOS
			table = 8
		elif req == "" and req1 == "" and req2 != "None" and req3 != "Todas":
			#SE INDICAN GRATUITO Y EVENTOS
			table = 9
		elif req != "" and req1 != "" and req2 != "None" and req3 == "Todas":
			#SE INDICAN FECHA INI FECHA FIN Y  GRATUITO
			table = 10
		elif req != "" and req1 != "" and str(req2) == "None" and req3 != "Todas":
			#SE INDICAN FECHA INI FECHA FIN Y EVENTOS
			table = 11
		elif req != "" and req1 == "" and req2 != "None" and req3 != "Todas":
			#SE INDICAN FECHA INI GRATUITO Y EVENTOS
			table = 12
		elif req == "" and req1 != "" and req2 != "None" and req3 != "Todas":
			#SE INDICAN FECHA FIN GRATUITO Y EVENTOS
			table = 13
		elif req != "" and req1 != "" and req2 != "None" and req3 != "Todas":
			#SE INDICAN FECHA INI FECHA FIN GRATUITO Y EVENTOS
			table = 14

		return "<p>Init:"+str(req)+ "    Fin: "+str(req1)+"     Gat: "+str(req2)+"      Local: "+str(req3)+ " Table: "+str(table)+"</p>"

	else:
		table = query_inicial()
		return render_template('index.html',headers=headers, objects=table)




def query_inicial():
	RDFsource = "https://raw.githubusercontent.com/pablo-crucera/Curso2021-2022-ODKG/master/HandsOn/eventosfinal-deverdad.ttl"
	g = Graph()
	g.namespace_manager.bind('ns', Namespace("http://www.example.org#"), override=False)
	g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
	g.namespace_manager.bind('xsd', Namespace("http://www.w3.org/2001/XMLSchema#"), override=False)
	g.namespace_manager.bind('smart', Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#"), override=False)
	g.parse(RDFsource, format="ttl")
	smart = Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#")
	xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
	q = prepareQuery('''
		SELECT ?title ?startDate ?location ?endDate ?price ?link WHERE {
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




def buscarEventosGratuitos():
	RDFsource = "https://raw.githubusercontent.com/pablo-crucera/Curso2021-2022-ODKG/master/HandsOn/eventosfinal-deverdad.ttl"
	g = Graph()
	g.namespace_manager.bind('ns', Namespace("http://www.example.org#"), override=False)
	g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
	g.namespace_manager.bind('xsd', Namespace("http://www.w3.org/2001/XMLSchema#"), override=False)
	g.namespace_manager.bind('smart', Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#"), override=False)
	g.parse(RDFsource, format="ttl")
	smart = Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#")
	xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
	q = prepareQuery('''
		SELECT ?title ?startDate ?location ?endDate ?price ?link WHERE {
        ?event a smart:Event.
        ?event smart:title ?title.
        ?event smart:startDate ?startDate.
        ?event smart:takesPlaceIn ?facility.
        ?facility smart:name ?location.
        ?event smart:endDate ?endDate.
        ?event smart:price ?price.
        ?event smart:URI ?link.
        ?event smart:free "true"^^xsd:boolean
      	}
    	''',
		initNs = { "smart": smart, "xsd": xsd}
	)

	queryOut = g.query(q)
	return queryOut


###### QUERY TIPO DE EVENTO #######

def buscarTipoDeEvento(nombre_tipo):
	# Introducir nombre del tipo en formato string
	RDFsource = "https://raw.githubusercontent.com/pablo-crucera/Curso2021-2022-ODKG/master/HandsOn/eventosfinal-deverdad.ttl"
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
		 ?event smart:URI ?link.
		 ?event smart:isA ?category.
		 ?category smart:name "'''+ nombre_tipo + '''"
		}
		''',
		initNs = { "smart": smart, "xsd": xsd}
	)

	queryOut = g.query(q)

	return(g.query(q))
