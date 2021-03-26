from flask import Flask, render_template, url_for, request
from rdflib import Graph, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery
from JSONLD import *

app = Flask(__name__)

PREFIX = 'PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>'
ELECTRIC_CARS_API_URL = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=300&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep"
ELECTRIC_CARS_CONTEXT = r'contexts/electric_car_parks.json'

CARS_API_URL = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=stations-services-en-france%40datanova&q=&facet=typeroute&facet=commune&facet=codepostal&facet=services&facet=carburants&facet=activite&rows=300"
CARS_CONTEXT = r'contexts/car_parks.json'


@app.route('/', methods=['GET', 'POST'])
def index():

    electric_cars_jsonLD = JSONLD(ELECTRIC_CARS_CONTEXT, ELECTRIC_CARS_API_URL)
    g = Graph().parse(data=electric_cars_jsonLD, format="json-ld")

    # Queries
    zipcode_query = """SELECT ?zipcode WHERE {
                ?a <http://www.owl-ontologies.com/stations-velos.owl#station> ?id .
                ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
                ?stationID <http://www.owl-ontologies.com/stations-velos.owl#zipcode> ?zipcode .
            }"""

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
        }"""

    all_zipcodes = []
    zipcodes = []
    data = []

    for _ in g.query(zipcode_query):
        all_zipcodes.append(_.zipcode.toPython())

    if request.method == 'POST':
        code = Literal(request.form['search'])
        q = prepareQuery(query)
        for _ in g.query(q, initBindings={'zipcode': code}):
            record = {
                "name": _.name.toPython(),
                "adress": _.add.toPython(),
                "zipcode":  _.zipcode.toPython(),
                "paying": _.payant.toPython(),
                "lat": _.lat.toPython(),
                "lon": _.lon.toPython(),
                "numberPlugs": _.numberPlugs.toPython(),
            }
            data.append(record)

    else:
        for _ in g.query(query):
            record = {
                "name": _.name.toPython(),
                "adress": _.add.toPython(),
                "zipcode": _.zipcode.toPython(),
                "paying": _.payant.toPython(),
                "lat": _.lat.toPython(),
                "lon": _.lon.toPython(),
                "numberPlugs": _.numberPlugs.toPython(),
            }
            data.append(record)
        print("GET  :" + str(len(data)))
    zipcodes = all_zipcodes

    print(len(data))
    return render_template('index.html', all_zipcodes=all_zipcodes, zipcodes=zipcodes, data=data)


@app.route('/essence', methods=['GET', 'POST'])
def termique():

    cars_jsonLD = JSONLD(CARS_CONTEXT, CARS_API_URL)
    g = Graph().parse(data=cars_jsonLD, format="json-ld")

    # Queries
    zipcode_query = """SELECT ?zipcode WHERE {
                ?a <http://www.owl-ontologies.com/stations-velos.owl#station> ?id .
                ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
                ?stationID <http://www.owl-ontologies.com/stations-velos.owl#zipcode> ?zipcode .
            }"""

    query = """PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>
        SELECT ?add ?insee ?lat ?lon
        WHERE {
            ?a st:station ?id .
            ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
            ?vraiID st:address ?add .
            ?vraiID st:zipcode ?insee .
            ?vraiID st:latlng ?lat .
            ?vraiID st:latlng ?lon .
            FILTER(?lat > ?lon)
        }"""

    all_zipcodes = []
    zipcodes = []
    data = []

    for _ in g.query(zipcode_query):
        all_zipcodes.append(_.zipcode.toPython())

    for _ in g.query(query):
        record = {
            "adress": _.add.toPython(),
            "zipcode": _.insee.toPython(),
            "lat": _.lat.toPython(),
            "lon": _.lon.toPython(),
        }
        data.append(record)

    if request.method == 'POST':
        indexes = [index for index, value in enumerate(
            all_zipcodes) if value == request.form['search']]
        zipcodes = [all_zipcodes[i] for i in indexes]

    else:
        zipcodes = all_zipcodes

    print(len(data))
    return render_template('index2.html', all_zipcodes=all_zipcodes, zipcodes=zipcodes, data=data)


if __name__ == '__main__':
    app.run(port="5000", debug=True)
