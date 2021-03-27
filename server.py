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


def parse_data(item):
    regex = re.match('^http', item.isElectrical.value)
    isElectrical = False if regex is None else True
    record = {
        "adress": item.add.value,
        "zipcode": item.zipcode.value,
        "lat": item.lat.value,
        "lon": item.lon.value,
        "isElectrical": isElectrical,

        "name": "" if item.name is None else item.name.value,
        "services": "" if item.services is None else item.services.value,
        "city": "" if item.city is None else item.city.value,
        "fuel": "" if item.fuel is None else item.fuel.value,
        "paying": "" if item.isPayant is None else item.isPayant.value,
        "numberPlugs": "" if item.numberPlugs is None else item.numberPlugs.value,
    }
    return record


def check_filters():
    if request.form.get('type_of_car'):
        checked = request.form.getlist('type_of_car')

        if 'electric' in checked and 'thermic' not in checked:
            query = Queries.ELECTRIC_CARS_ONLY.value

        elif 'thermic' in checked and 'electric' not in checked:
            query = Queries.THERMIC_CARS_ONLY.value

        else:
            query = Queries.ALL_CARS.value

    else:
        query = Queries.ALL_CARS.value

    return query


@app.route('/', methods=['GET', 'POST'])
def index():

    # Queries
    zipcode_query = Queries.ALL_ZIPCODES.value
    query = Queries.ALL_CARS.value
    data = []
    all_zipcodes = []

    for _ in g.query(zipcode_query):
        all_zipcodes.append(_.zipcode.value)

    if request.method == 'POST':
        if request.form['search']:
            code = Literal(request.form['search'])
            query = check_filters()
            q = prepareQuery(query)

            for item in g.query(q, initBindings={'zipcode': code}):
                data.append(parse_data(item))

        else:
            query = check_filters()

            for item in g.query(query):
                data.append(parse_data(item))

    else:
        for item in g.query(query):
            data.append(parse_data(item))

    return render_template('index.html', all_zipcodes=all_zipcodes, data=data)


if __name__ == '__main__':
    app.run(port="5000", debug=True)
