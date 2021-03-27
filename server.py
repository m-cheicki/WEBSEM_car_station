import re
from flask import Flask, render_template, url_for, request
from rdflib import Graph, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery
from JSONLD import *
from Queries import *

app = Flask(__name__)

ELECTRIC_CARS_API_URL = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&rows=300&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep"
ELECTRIC_CARS_CONTEXT = r'contexts/electric_car_parks.json'

CARS_API_URL = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=stations-services-en-france%40datanova&q=&facet=typeroute&facet=commune&facet=codepostal&facet=services&facet=carburants&facet=activite&rows=300"
CARS_CONTEXT = r'contexts/car_parks.json'

electric_cars_jsonLD = JSONLD(ELECTRIC_CARS_CONTEXT, ELECTRIC_CARS_API_URL)
cars_jsonLD = JSONLD(CARS_CONTEXT, CARS_API_URL)

g = Graph()
g.parse(data=electric_cars_jsonLD, format="json-ld")
g.parse(data=cars_jsonLD, format="json-ld")


def parse_data(graph, query):
    data = []
    for _ in graph.query(query):
        regex = re.match('^http', _.isElectrical.value)
        isElectrical = False if regex is None else True
        record = {
            "adress": _.add.value,
            "zipcode": _.zipcode.value,
            "lat": _.lat.value,
            "lon": _.lon.value,
            "isElectrical": isElectrical,

            "name": "" if _.name is None else _.name.value,
            "services": "" if _.services is None else _.services.value,
            "city": "" if _.city is None else _.city.value,
            "fuel": "" if _.fuel is None else _.fuel.value,
            "paying": "" if _.isPayant is None else _.isPayant.value,
            "numberPlugs": "" if _.numberPlugs is None else _.numberPlugs.value,
        }
        data.append(record)
    return data


@app.route('/', methods=['GET', 'POST'])
def index():

    # Queries
    zipcode_query = Queries.ALL_ZIPCODES.value
    query = Queries.ELECTRIC_CARS_ONLY.value
    init_query = Queries.ALL_CARS.value
    data = []
    all_zipcodes = []

    for _ in g.query(zipcode_query):
        all_zipcodes.append(_.zipcode.value)

    if request.method == 'POST':
        if request.form['type_of_car']:
            checked = request.form.getlist('type_of_car')
            if 'electric' in checked and 'thermic' not in checked:
                print("electric cars")
            elif 'thermic' in checked and 'electric' not in checked:
                print('thermic')
            else:
                print("NONE OR BOTH")

        code = Literal(request.form['search'])
        q = prepareQuery(query)
        for _ in g.query(q, initBindings={'zipcode': code}):
            record = {
                "name": _.name.value,
                "adress": _.add.value,
                "zipcode":  _.zipcode.value,
                "paying": _.payant.value,
                "lat": _.lat.value,
                "lon": _.lon.value,
                "numberPlugs": _.numberPlugs.value,
            }
            data.append(record)

    else:
        data = parse_data(g, init_query)

    return render_template('index.html', all_zipcodes=all_zipcodes, data=data)


if __name__ == '__main__':
    app.run(port="5000", debug=True)
