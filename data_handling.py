def api_preprocess_datapoint(data):
    ddata = data.copy()
    result = ddata.pop('result')
    return result, ddata
