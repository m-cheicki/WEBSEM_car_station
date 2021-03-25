import requests
from rdflib import Graph
from JSONLD import *


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

URL = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=10&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep"

jsonld = JSONLD(r'contexts/electric_car_parks.json', URL)
g = Graph().parse(data=jsonld, format="json-ld")

for _ in g.query(query):
    a.append(_)
    print(_)
