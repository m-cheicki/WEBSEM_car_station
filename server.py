import re
from flask import Flask, render_template, request
from flask_minify import minify
from rdflib import Graph, Literal
from rdflib.plugins.sparql import prepareQuery
from JSONLD import *
from Queries import *

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)

######################################
# CALL APIs AND PARSING INTO JSON-LD
######################################
NUMBER_OF_RESULTS = 10000

ELECTRIC_CARS_API_URL = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep&rows=" + \
    str(NUMBER_OF_RESULTS)

ELECTRIC_CARS_API_URL_PART1 = f"{ELECTRIC_CARS_API_URL}&start=0"
ELECTRIC_CARS_API_URL_PART2 = f"{ELECTRIC_CARS_API_URL}&start={NUMBER_OF_RESULTS}"
ELECTRIC_CARS_API_URL_PART3 = f"{ELECTRIC_CARS_API_URL}&start={NUMBER_OF_RESULTS*2}"

ELECTRIC_CARS_CONTEXT = r'contexts/electric_car_parks.json'

CARS_API_URL = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=stations-services-en-france%40datanova&q=&facet=typeroute&facet=commune&facet=codepostal&facet=services&facet=carburants&facet=activite&rows=" + \
    str(NUMBER_OF_RESULTS)

CARS_API_URL_PART1 = f"{CARS_API_URL}&start=0"
CARS_API_URL_PART2 = f"{CARS_API_URL}&start={NUMBER_OF_RESULTS}"

CARS_CONTEXT = r'contexts/car_parks.json'

electric_cars_jsonLD1 = JSONLD(
    ELECTRIC_CARS_CONTEXT, ELECTRIC_CARS_API_URL_PART1)
electric_cars_jsonLD2 = JSONLD(
    ELECTRIC_CARS_CONTEXT, ELECTRIC_CARS_API_URL_PART2)
electric_cars_jsonLD3 = JSONLD(
    ELECTRIC_CARS_CONTEXT, ELECTRIC_CARS_API_URL_PART3)

cars_jsonLD1 = JSONLD(CARS_CONTEXT, CARS_API_URL_PART1)
cars_jsonLD2 = JSONLD(CARS_CONTEXT, CARS_API_URL_PART2)

######################################
# GENERATE GRAPH
######################################
g = Graph()
g.parse(data=electric_cars_jsonLD1, format="json-ld")
g.parse(data=electric_cars_jsonLD2, format="json-ld")
g.parse(data=electric_cars_jsonLD3, format="json-ld")
g.parse(data=cars_jsonLD1, format="json-ld")
g.parse(data=cars_jsonLD2, format="json-ld")


# Parse data to return to the view
def parse_data(item):
    regex = re.match('^http', item.isElectrical.value)
    isElectrical = False if regex is None else True
    record = {
        "address": item.add.value.replace('\n\r', ' ').replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' '),
        "zipcode": item.zipcode.value,
        "lat": item.lat.value,
        "lon": item.lon.value,
        "isElectrical": isElectrical,
        "name": "" if item.name is None else item.name.value,
        "services": "" if item.services is None else item.services.value.replace('|', ', '),
        "city": "" if item.city is None else item.city.value,
        "fuel": "" if item.fuel is None else item.fuel.value.replace('|', ', '),
        "paying": "" if item.isPayant is None else item.isPayant.value,
        "numberPlugs": "" if item.numberPlugs is None else item.numberPlugs.value,
    }
    return record


# Check filters for searchbar : return the query
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# if __name__ == '__main__':
#     app.run(port="5000", debug=True)
