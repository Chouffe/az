import flask
import settings
import json
import db
import ml
import data_handling
import generator
import requests
import random
import experiments

app = flask.Flask(__name__, static_url_path='')


@app.route('/api/<string:uuid>', methods=['GET'])
def next_point(uuid):
    """Given the uuid of the schema, it returns the next_point based
    on the current schema and the already seen datapoints
    eg. {feature1: value1, feature2: value2, ...}"""
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    base_url = "http://localhost:%s/service/predict/" % settings.ml_service_port

    schema = db.get_schema(uuid)
    features = schema['features']
    dataset = data_handling.datapoints_to_dataset(db.get_datapoints(uuid))

    gen = generator.RandomGenerator(features)
    number_points_to_try = random.randint(50, 500)
    points_to_try = gen.get(n=number_points_to_try)

    if len(dataset) > settings.min_points_for_smbo:
        train, target = data_handling.dataset_to_matrix(features, dataset)

        r = requests.post(base_url + uuid,
                          data=json.dumps({'points': points_to_try}),
                          headers=headers)
        request_results = r.json()

        scores = ml.score_mu_sigma(target,
                                   request_results['mu'],
                                   request_results['sigma'])

        order = True if settings.optimization_strategy == 'maximize' else False
        top_ei, top_point = sorted(zip(scores, points_to_try),
                                   key=lambda x: x[0],
                                   reverse=order)[0]
        return json.dumps(top_point)
    else:
        # Returns a random point
        return json.dumps(points_to_try[0])


@app.route('/api/<string:uuid>', methods=['POST'])
def save_point(uuid):
    """Saves the datapoint sent and returns success or an error message
    It needs to contain the 'result' key with a value associated with it
    input: {feature1: value1, feature2: value2, ..., result: valueR}
    """
    schema = db.get_schema(uuid)
    data = flask.request.json
    if not schema:
        return json.dumps({'error': 'No schema with uuid: %s' % uuid})
    if 'result' not in data:
        return json.dumps({'error':
                           'Error in the input -> the result key is needed'})
    result, features = data_handling.api_preprocess_datapoint(data)
    schema_feature_set = set(schema['features'].keys())
    input_feature_set = set(features)
    if schema_feature_set != input_feature_set:
        return json.dumps({'error':
                           'Error in the input -> The datapoints lacks some keys %s' % (schema_feature_set - input_feature_set)})
    if not data or result is None or not features:
        flask.abort(400)  # bad request
    try:
        # Save the datapoint
        db.write_datapoint(uuid, features, result)
        return json.dumps({'error': None})
    except:
        return json.dumps({'error': 'An error occured'})


@app.route('/api/schemas', methods=['GET'])
def get_schemas():
    """Returns the schemas"""
    schemas = db.get_schemas()

    for schema in schemas:
        schema.pop('_id', None)

    return json.dumps({'schemas': schemas})


@app.route('/api/schema/<string:uuid>', methods=['GET'])
def get_schema(uuid):
    """Returns the schema"""
    schema = db.get_schema(uuid)
    if not schema:
        return json.dumps({'error': 'No schema with uuid: %s' % uuid})
    else:
        schema.pop('_id', None)
        return json.dumps(schema)


@app.route('/api/schema/<string:uuid>', methods=['POST', 'OPTIONS'])
def create_schema(uuid):
    """Creates a schema given the features
    Input:
        - features
    """
    data = flask.request.json
    if not data:
        flask.abort(400)  # bad request
    try:
        db.write_schema(uuid, data.get('features', []))
    except:
        return json.dumps({'error': 'An error occured'})
    return json.dumps({'error': None})


@app.route('/api/schema/<string:uuid>', methods=['DELETE'])
def delete_schema(uuid):
    """Deletes a schema + its datapoints"""
    try:
        db.delete_schema(uuid)
        db.delete_datapoints(uuid)
    except:
        return json.dumps({'error': 'An error occured'})
    return json.dumps({'error': None})


@app.route('/api/feature/<string:uuid>', methods=['POST', 'OPTIONS'])
def add_feature(uuid):
    """Adds a new feature"""
    data = flask.request.json
    if not data:
        flask.abort(400)  # bad request
    try:
        # Save the datapoint
        db.add_feature(uuid, data)
        return json.dumps({'error': None})
    except:
        return json.dumps({'error': 'An error occured'})


@app.route('/api/feature/<string:uuid>', methods=['DELETE'])
def remove_feature(uuid):
    """Deletes a new feature"""
    data = flask.request.json
    if not data or not data.get('feature_name', None):
        flask.abort(400)  # bad request
    else:
        db.remove_feature(uuid, data['feature_name'])
        return json.dumps({'error': None})

if __name__ == '__main__':
    app.run(port=settings.server_port)
