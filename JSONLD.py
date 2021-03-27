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


def createJSONLD(context_file_path, request_response):
    context = ""
    data_buffer = open(context_file_path, 'r')

    # Convert buffer to str
    try:
        str += data_buffer
    except Exception as e:
        pass
    context += data_buffer.read()

    return context[:-1] + "," + request_response[1:len(request_response)]
