import requests
from rdflib import Graph, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


from JSONLD import *

PREFIX = 'PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>'
URL = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=10000&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep"

jsonld = JSONLD(r'contexts/electric_car_parks.json', URL)
g = Graph().parse(data=jsonld, format="json-ld")

a = []
query = """PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>
    SELECT ?add ?insee ?name ?payant ?lat ?lon ?numberPlugs
    WHERE {
        ?a st:station ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID st:address ?add .
        ?vraiID st:zipcode ?insee .
        ?vraiID st:name ?name .
        ?vraiID st:isPayant ?payant .
        ?vraiID st:numberPlugs ?numberPlugs .
        ?vraiID st:coordonnees ?lat .
        ?vraiID st:coordonnees ?lon .
        FILTER(?lat > ?lon)
    } LIMIT 1"""

# for _ in g.query(query):
#     a.append(_)
#     print(_)


specific_zipcode2 = PREFIX + """SELECT ?add ?name ?payant ?lat ?lon ?numberPlugs
    WHERE {
        ?a st:station ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID st:address ?add .
        ?vraiID st:zipcode '75113' .
        ?vraiID st:name ?name .
        ?vraiID st:isPayant ?payant .
        ?vraiID st:numberPlugs ?numberPlugs .
        ?vraiID st:coordonnees ?lat .
        ?vraiID st:coordonnees ?lon .
        FILTER(?lat > ?lon)
    }"""

test = PREFIX + """SELECT ?zipcode
    WHERE {
        ?a st:station ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID st:zipcode ?zipcode .
    }LIMIT 1"""

query = PREFIX + """SELECT ?add ?name ?payant ?lat ?lon ?numberPlugs ?zipcode
    WHERE {
        ?a st:station ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID st:address ?add .
        ?vraiID st:zipcode ?zipcode .
        ?vraiID st:name ?name .
        ?vraiID st:isPayant ?payant .
        ?vraiID st:numberPlugs ?numberPlugs .
        ?vraiID st:coordonnees ?lat .
        ?vraiID st:coordonnees ?lon .
        FILTER(?lat > ?lon)
    } LIMIT 1"""

code = Literal("75113")
q = prepareQuery(query)

for _ in g.query(q, initBindings={'zipcode': code}):
    print(_)
