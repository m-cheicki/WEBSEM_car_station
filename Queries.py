from enum import Enum

PREFIX = "PREFIX st:<https://car-station.mcheicki.com/ontology/electric_ontology.owl#>"


class Queries(Enum):
    ALL_CARS = PREFIX + """SELECT DISTINCT
        ?name ?add ?zipcode ?lat ?lon ?isElectrical ?services ?city ?fuel ?isPayant ?numberPlugs
        WHERE {
            ?a st:station ?id .
            ?id <https://car-station.mcheicki.com/ontology/electric_ontology.owl#@nest> ?stationID .
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
        } LIMIT 500"""

    THERMIC_CARS_ONLY = PREFIX + """SELECT DISTINCT ?name ?add ?zipcode ?lat ?lon ?isElectrical ?services ?city ?fuel ?isPayant ?numberPlugs
        WHERE {
            ?a st:station ?id .
            ?id <https://car-station.mcheicki.com/ontology/electric_ontology.owl#@nest> ?stationID .
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
        } LIMIT 100
    """

    ELECTRIC_CARS_ONLY = PREFIX + """SELECT DISTINCT ?name ?add ?zipcode ?lat ?lon ?isElectrical ?services ?city ?fuel ?isPayant ?numberPlugs
        WHERE {
            ?a st:station ?id .
            ?id <https://car-station.mcheicki.com/ontology/electric_ontology.owl#@nest> ?stationID .
            ?stationID st:address ?add .
            ?stationID st:zipcode ?zipcode .
            ?stationID st:coordonnees ?lat .
            ?stationID st:coordonnees ?lon .
            ?stationID st:isElectrical ?isElectrical .
            ?stationID st:isPayant ?isPayant .
            ?stationID st:numberPlugs ?numberPlugs .
            ?stationID st:name ?name .

            FILTER(?lat > ?lon)
        } LIMIT 500
    """

    ALL_ZIPCODES = PREFIX + """SELECT DISTINCT ?zipcode WHERE {
            ?a st:station ?id .
            ?id <https://car-station.mcheicki.com/ontology/electric_ontology.owl#@nest> ?stationID .
            ?stationID st:zipcode ?zipcode .
        }"""
