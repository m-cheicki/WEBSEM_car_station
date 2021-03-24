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

    "id_station": "@id",
    "n_enseigne": "name",
    "xlongitude": "lon",
    "ylatitude": "lat",
    "code_insee": "zipcode",
    "ad_station": "address",
    "nbre_pdc": "numberPlugs",
    "acces_recharge": "shouldPay",
    "fields":"@nest",
    "parameters": "@nest",
    "records":{"@id":"station"}, 

    "datasetid": null,
    "recordid": null,
    "horaires_sav": null,
    "tel_sav": null,
    "type_prise": null,
    "n_station": null,
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
    "facet_groups" : null
  },'''

r = requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=10000&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep")
j = r.text

# Transform JSON to JSON-LD adding context
j = "{"+context+j[1:len(j)]

# Create graph from JSON-LD
g = Graph().parse(data=j, format="json-ld")

# Querying Graph
for _ in g.query("""SELECT ?id ?add
    WHERE {
        ?a <http://www.owl-ontologies.com/stations-velos.owl#station> ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#zipcode> ?add .
    }"""):
    print(_.add.toPython())
