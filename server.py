import flask
import settings
import json
import db
import ml
import data_handling
import generator

app = flask.Flask(__name__)


@app.route('/api/<string:uuid>', methods=['GET'])
def next_point(uuid):
    """Given the uuid of the schema, it returns the next_point based
    on the current schema and the already seen datapoints
    eg. {feature1: value1, feature2: value2, ...}"""
    # --------------------------------------------
    # TODO
    # - Generate new points to try
    #     -> Be smarter about it
    #     - Annealing
    #     - Generative models
    #     - Hill climbing methods
    # - Fit a model based on the data already seen
    #    -> For now a random forest
    #    -> Extend to any Regressor by boostraping
    #         -> Implement my own bootstraping method
    # - Predict the best points to try next
    #    -> Exploration vs exploitation
    # - Return the best one
    # --------------------------------------------
    # Returns a random point drawn form the schema distribution
    schema = db.get_schema(uuid)
    features = schema['features']
    dataset = data_handling.datapoints_to_dataset(db.get_datapoints(uuid))
    train, target = data_handling.dataset_to_matrix(features, dataset)
    gen = generator.RandomGenerator(features)
    points_to_try = gen.get(n=100)

    if len(dataset) > settings.min_points_for_smbo:
        # Fits a ML Model to predict the best point to try next
        vectors = data_handling.points_to_vectors(points_to_try, features)
        train, target = data_handling.dataset_to_matrix(features, dataset)
        scores, importances = ml.score_points(train, target, vectors)
        # Need to sort in reverse because we are maximizing the objective function
        top_ei, top_vector = sorted(zip(scores, vectors), key=lambda x: x[0], reverse=True)[0]
        return json.dumps(data_handling.vector_to_point(top_vector, features))
    # Returns a random point
    else:
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


@app.route('/api/schema/<string:uuid>', methods=['GET'])
def get_schema(uuid):
    """Returns the schema"""
    schema = db.get_schema(uuid)
    # print "SCHEMA: ", schema
    if not schema:
        return json.dumps({'error': 'No schema with uuid: %s' % uuid})
    else:
        schema.pop('_id', None)
        return json.dumps(schema)


@app.route('/api/schema/<string:uuid>', methods=['POST'])
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


@app.route('/api/feature/<string:uuid>', methods=['POST'])
def add_feature(uuid):
    """Adds a new feature"""
    data = flask.request.json
    # print "DATA:", data
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
    """Adds a new feature"""
    data = flask.request.json
    if not data or not data.get('feature_name', None):
    db.remove_feature(uuid, data['feature_name'])


if __name__ == '__main__':
    app.run(port=settings.server_port)
