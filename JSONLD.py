import requests


class JSONLD:
    def __init__(self):
        pass

    def __new__(cls, context, URL):
        req = requestAPI(URL)
        return createJSONLD(context, req)


def requestAPI(URL):
    r = requests.get(URL)
    return r.text


def createJSONLD(context, request_response):
    return "{" + context + request_response[1:len(request_response)]
