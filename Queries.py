from enum import Enum

PREFIX = "PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>"


class Queries(Enum):
    COMMON_INFORMATION = PREFIX + """SELECT
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
    ALL_INFORMATION_FOR_THERMICS = PREFIX + """SELECT ?add ?insee ?lat ?lon
        WHERE {
            ?a st:station ?id .
            ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
            ?vraiID st:address ?add .
            ?vraiID st:zipcode ?insee .
            ?vraiID st:latlng ?lat .
            ?vraiID st:latlng ?lon .
            FILTER(?lat > ?lon)
        }"""

    ALL_INFORMATION_FOR_ELECTRICS = PREFIX + """SELECT ?add ?name ?payant ?lat ?lon ?numberPlugs ?zipcode
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

    ALL_ZIPCODES = PREFIX + """SELECT ?zipcode WHERE {
            ?a st:station ?id .
            ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?stationID .
            ?stationID st:zipcode ?zipcode .
        }"""
