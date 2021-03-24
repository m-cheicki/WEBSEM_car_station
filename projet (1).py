import requests
from rdflib import Graph

context_original='''"@context" : {
    "@vocab":"http://www.owl-ontologies.com/stations-velos.owl#",
    "@base":"http://www.owl-ontologies.com/stations-velos.owl/",
    "nhits" : "total",
    "rows" : "nbquery",
    "start" : "debut",
    "dataset" : null,
    "timezone": null,
    "format": null,
    "facet": null,

    "datasetid": null,
    "recordid": null,
    "ylatitude": "lat",
    "horaires_sav": null,
    "tel_sav": null,
    "type_prise": null,
    "n_station": null,
    "xlongitude": "lon",
    "n_amenageur": null,
    "id_pdc": null,
    "ad_station": "adresse",
    "date_maj": null,
    "geo_point_2d": null,
    "accessibilite": null,
    "puiss_max": null,
    "id_station": "@id",
    "observations": null,
    "code_insee": null,
    "nbre_pdc": "nombrePrise",
    "n_operateur": null,
    "acces_recharge": "isPayant",
    "n_enseigne": null,
    "geometry" : null,
    "record_timestamp": null,
    "facet_groups" : null,
    "fields":"@nest",
    "parameters": "@nest",
    "records":{"@id":"station"}
  },'''

context='''"@context": {
    "@vocab": "http://www.owl-ontologies.com/stations-velos.owl#",
    "@base": "http://www.owl-ontologies.com/stations-velos.owl/",
    "nhits": "total",
    "rows": "nbquery",
    "start": "debut",
    "dataset": null,
    "timezone": null,
    "format": null,
    "facet": null,

    "parameters": "@nest",
    "records": {
      "@id": "station"
    },
    "datasetid": null,
    "recordid": null,
    "fields": "@nest",
    "accessibilite": null,
    "n_enseigne": null,
    "type_prise": null,
    "code_insee": "code_insee",
    "puiss_max": "power",
    "n_amenageur": null,
    "ad_station": "adresse",
    "date_maj": null,
    "source": null,
    "observations": null,
    "id_station": null,
    "nbre_pdc": "nb",
    "n_station": "name",
    "id_pdc": "@id",
    "n_operateur": null,
    "coordonnees": {"@container":"id"},
    "acces_recharge": "isPayant"
  },'''

r=requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=10000&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep")
j=r.text

# Transform JSON to JSON-LD adding context
j="{"+context+j[1:len(j)]

# Create graph from JSON-LD
g=Graph().parse(data=j, format="json-ld")

# Querying Graph

a=[]
for _ in g.query("""SELECT ?add ?insee ?name ?payant ?nb ?lat ?lon
    WHERE {
        ?a <http://www.owl-ontologies.com/stations-velos.owl#station> ?id .
	?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#adresse> ?add .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#code_insee> ?insee .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#name> ?name .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#isPayant> ?payant .
	?vraiID <http://www.owl-ontologies.com/stations-velos.owl#nb> ?nb .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#coordonnees> ?lat .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#coordonnees> ?lon .
        FILTER(?lat > ?lon)
    }"""):
    a.append(_)



for _ in g.query("""SELECT ?id ?add
    WHERE {
        ?a <http://www.owl-ontologies.com/stations-velos.owl#station> ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID <http://www.owl-ontologies.com/stations-velos.owl#adresse> ?add .
    }"""):
    print(_)

for _ in g.query("""SELECT ?mid ?vraiID 
    WHERE {
        ?a <http://www.owl-ontologies.com/stations-velos.owl#station> ?id .
        ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
        ?vraiID ?mid ?add .
    }"""):
    print(_)

for _ in g.query(""" SELECT ?lat ?lon
    WHERE {
        <http://www.owl-ontologies.com/stations-velos.owl/FR*55C*E92380*48*838740*2*187189*1> <http://www.owl-ontologies.com/stations-velos.owl#coordonnees> ?lat .
        <http://www.owl-ontologies.com/stations-velos.owl/FR*55C*E92380*48*838740*2*187189*1> <http://www.owl-ontologies.com/stations-velos.owl#coordonnees> ?lon .
        FILTER(?lat > ?lon)
    }
"""):
    print(_)
<http://www.owl-ontologies.com/stations-velos.owl/FR*S11*P11288*001>
