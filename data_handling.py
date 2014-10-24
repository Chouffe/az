from db import get_datapoints


def api_preprocess_datapoint(data):
    ddata = data.copy()
    result = ddata.pop('result')
    return result, ddata


def process_datapoints(data):
    print [p for p in data]

print "YO"
process_datapoints(get_datapoints('test6'))
print "YO"
