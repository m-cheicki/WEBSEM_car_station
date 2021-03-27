import requests
from rdflib import Graph, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
import re

from JSONLD import *

PREFIX = 'PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>'
URL = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=1&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep"
CARS_API_URL = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=stations-services-en-france%40datanova&q=&facet=typeroute&facet=commune&facet=codepostal&facet=services&facet=carburants&facet=activite&rows=1"

jsonld = JSONLD(r'contexts/electric_car_parks.json', URL)
jsonld2 = JSONLD(r'contexts/car_parks.json', CARS_API_URL)
g = Graph()
g.parse(data=jsonld, format="json-ld")
g.parse(data=jsonld2, format="json-ld")

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

# code = Literal("75113")
# q = prepareQuery(query)

# for _ in g.query(q, initBindings={'zipcode': code}):
#     print(_)


COMMON_INFORMATION = PREFIX + """SELECT ?name ?add ?zipcode ?lat ?lon ?isElectrical ?services ?city ?fuel
        WHERE {
            ?a st:station ?id .
            ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
            ?stationID st:address ?add .
            ?stationID st:zipcode ?zipcode .
            ?stationID st:coordonnees ?lat .
            ?stationID st:coordonnees ?lon .
            ?stationID st:isElectrical ?isElectrical .
            OPTIONAL{
                ?stationID st:name ?name .
            }
            OPTIONAL{
                ?stationID st:services ?services .
            }
            OPTIONAL{
                ?stationID st:city ?city .
            }
            OPTIONAL{
                ?stationID st:fuel ?fuel .
            }
        
            FILTER(?lat > ?lon)
        }"""

THERMIC_CARS_ONLY = PREFIX + """SELECT DISTINCT ?add ?zipcode ?city ?services ?fuel ?isElectrical ?lat ?lon
    WHERE {
        ?a st:station ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
        ?stationID st:address ?add .
        ?stationID st:zipcode ?zipcode .
        ?stationID st:city ?city .
        ?stationID st:coordonnees ?lat .
        ?stationID st:coordonnees ?lon .

        VALUES ?isElectrical {'R' 'A' 'N'}
        ?stationID st:isElectrical ?isElectrical .

        OPTIONAL{
            ?stationID st:fuel ?fuel .
        }
        OPTIONAL{
            ?stationID st:services ?services .
        }
        FILTER(?lat > ?lon)
    }
"""

ELECTRIC_CARS_ONLY = PREFIX + """SELECT DISTINCT ?add ?name ?zipcode ?lat ?lon ?payant ?numberPlugs
    WHERE {
        ?a st:station ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
        ?stationID st:address ?add .
        ?stationID st:zipcode ?zipcode .
        ?stationID st:coordonnees ?lat .
        ?stationID st:coordonnees ?lon .
        ?stationID st:isElectrical ?isElectrical .
        ?stationID st:isPayant ?payant .
        ?stationID st:numberPlugs ?numberPlugs .
        ?stationID st:name ?name .

        FILTER(?lat > ?lon)
    }
"""

for _ in g.query(ELECTRIC_CARS_ONLY):
    print(_)
    print()

"""
?stationID st:isPayant ?payant .
?stationID st:numberPlugs ?numberPlugs .
? stationIDst: name ? name.
"""
