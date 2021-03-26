from enum import Enum

PREFIX = "PREFIX st:<http://www.owl-ontologies.com/stations-velos.owl#>"


class Queries(Enum):
    COMMON_INFORMATION = PREFIX + """SELECT ?add ?insee ?lat ?lon
        WHERE {
            ?a st:station ?id .
            ?id <http://www.owl-ontologies.com/stations-velos.owl#@nest> ?vraiID .
            ?vraiID st:address ?add .
            ?vraiID st:zipcode ?insee .
            ?vraiID st:latlng ?lat .
            ?vraiID st:latlng ?lon .
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
