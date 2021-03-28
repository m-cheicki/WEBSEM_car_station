# Car station

A4 ESILV - WEB DATAMINING AND SEMANTICS<br/>
Amar Merwan CHELOUAH - Kévin CELIE - Mariyam CHEICK ISMAIL

---

## How to use

As the project is hosted in a web server, just [click in the link](https://car-station.mcheicki.com/). <br/>
It takes some time, so don't worry, and wait few minutes :) <br/>
Once the web page is loaded, you can either choose to use your location or not. Then, you will be able to see all stations. <br/>
_For development purposes, we have decided to limit our main query to 500 results._

You can click on the left panel where there are all the results. It will show you the selected car station. <br/>
You can also filter by type of car: either thermic or electric. And also, you can enter a zipcode in the search bar. <br/>

### Demonstration video

<a href="https://car-station.mcheicki.com/public/DEMO_DIA4_GROUP5_CELIE_CHELOUAH_CHEICKISMAIL_WEBSEM.mp4" download>Click here to download the video</a>

## How to install

There is nothing to install as everything is online.

If you want to have a copy of the code, you can :

-   Fork this repo

OR

-   Clone this repo :
    `git clone https://github.com/m-cheicki/WEBSEM_car_station.git`
-   In the shell, go into the repository using `cd PATH_TO_REPO`
-   Install necessery packages by running the following command in the shell
    `pip install -r requirements.txt`
-   Open `server.py` file in your favorite code editor/IDE
-   Go at the end of the file, uncomment the two last lines in order to have :

```
if __name__ == '__main__':
    app.run(port="5000", debug=True)
```

-   Run the server by typing `python server.py`
-   Open a web browser like Chrome and go to [this URL: http://localhost:5000/](http://localhost:5000/)
-   Wait few seconds, and here you are! The app is loading

**NOTE : As the server has the version 3.8.6 of Python we strongly recommand to have this version or higher**

## Our APIs

To realise this project we have used two APIs :

-   [Electric car stations](https://public.opendatasoft.com/explore/dataset/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve/table/?flg=fr)
-   [Thermic car stationns](https://data.opendatasoft.com/explore/dataset/stations-services-en-france%40datanova/api/?flg=fr&disjunctive.typeroute&disjunctive.commune&disjunctive.codepostal&disjunctive.services&disjunctive.carburants&disjunctive.activite)

The first one gives us more than 20,000 entries and the second one around 10,000 which gives us a total of 30,000 data approximatively. <br/>

## Our ontology

Our ontology is available [here](https://electric-car-park.mcheicki.com/ontology/ontology.owl).
<a href="https://electric-car-park.mcheicki.com/ontology/ontology.owl" download>You can download it here.</a>

## Structure

-   `contexts` contains our APIs context for JSON-LD
-   `JSONLD.py` is a file that parse our API into a JSON-LD using its context defined in the context folder
-   `Queries.py` is a file with our SPARQL queries
-   `static` and `templates` are folder used by Flask
