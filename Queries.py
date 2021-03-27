from enum import Enum

PREFIX = "PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>"


class Queries(Enum):
    ALL_CARS = PREFIX + """SELECT
        ?name ?add ?zipcode ?lat ?lon ?isElectrical ?services ?city ?fuel ?isPayant ?numberPlugs
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
            OPTIONAL{
                ?stationID st:isPayant ?isPayant .
            }
            OPTIONAL{
                ?stationID st:numberPlugs ?numberPlugs .
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

    ALL_ZIPCODES = PREFIX + """SELECT ?zipcode WHERE {
            ?a st:station ?id .
            ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
            ?stationID st:zipcode ?zipcode .
        }"""
