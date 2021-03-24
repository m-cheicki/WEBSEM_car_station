import requests
from rdflib import Graph

context = '''"@context" : {
    "@vocab":"http://www.owl-ontologies.com/stations-velos.owl#",
    "@base":"http://www.owl-ontologies.com/stations-velos.owl/",
    "nhits" : "total",
    "rows" : "nbquery",
    "start" : "start",
    "dataset" : null,
    "timezone": null,
    "format": null,
    "facet": null,

    "id_pdc": "@id",
    "n_station": "name",
    "xlongitude": "lon",
    "ylatitude": "lat",
    "code_insee": "zipcode",
    "ad_station": "address",
    "nbre_pdc": "numberPlugs",
    "acces_recharge": "isPayant",
    "fields":"@nest",
    "parameters": "@nest",
    "records":{"@id":"station"}, 
    "coordonnees": {"@container":"id"},
    "isElectrical": "1", 

    "id_station": null,
    "datasetid": null,
    "recordid": null,
    "horaires_sav": null,
    "tel_sav": null,
    "type_prise": null,
    "n_enseigne": null,
    "n_amenageur": null,
    "id_pdc": null,
    "date_maj": null,
    "geo_point_2d": null,
    "accessibilite": null,
    "puiss_max": null,
    "observations": null,
    "n_operateur": null,
    "geometry" : null,
    "record_timestamp": null,
    "source": null,
    "facet_groups" : null
},'''

r = requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=10000&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep")
j = r.text

# Transform JSON to JSON-LD adding context
j = "{"+context+j[1:len(j)]

# Create graph from JSON-LD
g = Graph().parse(data=j, format="json-ld")

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
    }"""

# Querying Graph
for _ in g.query(query):
    a.append(_)
