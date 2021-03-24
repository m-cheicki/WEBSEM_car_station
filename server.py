from flask import Flask, render_template, url_for, request
import requests
from rdflib import Graph

API_URL = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=10000&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep"

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

r = requests.get(API_URL)
j = r.text

# Transform JSON to JSON-LD adding context
j = "{"+context+j[1:len(j)]

# Create graph from JSON-LD
g = Graph().parse(data=j, format="json-ld")

# Queries
zipcode_query = """SELECT ?zipcode WHERE {
            ?a <http://www.owl-ontologies.com/stations-velos.owl#station> ?id .
            ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
            ?stationID <http://www.owl-ontologies.com/stations-velos.owl#zipcode> ?zipcode .
        }"""

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


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    all_zipcodes = []
    zipcodes = []
    data = []

    for _ in g.query(zipcode_query):
        all_zipcodes.append(_.zipcode.toPython())

    for _ in g.query(query):
        record = {
            "name": _.name.toPython(),
            "adress": _.add.toPython(),
            "zipcode": _.insee.toPython(),
            "paying": _.payant.toPython(),
            "lat": _.lat.toPython(),
            "lon": _.lon.toPython(),
            "numberPlugs": _.numberPlugs.toPython(),
        }
        data.append(record)

    if request.method == 'POST':
        indexes = [index for index, value in enumerate(
            all_zipcodes) if value == request.form['search']]
        zipcodes = [all_zipcodes[i] for i in indexes]

    else:
        zipcodes = all_zipcodes

    print(len(data))
    return render_template('index.html', all_zipcodes=all_zipcodes, zipcodes=zipcodes, data=data)


if __name__ == '__main__':
    app.run(port="5000", debug=True)
