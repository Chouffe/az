import flask

import settings
import json
import db
import ml
import utils
import data_handling

service = flask.Flask(__name__)


def cache_model(get_model):

    max_cache = 5  # 5 s caching
    models_dict = {}

    def f(uuid):
        if uuid in models_dict:
            if (utils.now() - models_dict[uuid]['date']).seconds < max_cache:
                print "OK"
                return models_dict[uuid]['model']
            else:
                # Retrain the model in another process asynchronously
                # Return the current model
                # TODO:
                print "KO2"
                models_dict[uuid] = {
                    'model': get_model(uuid),
                    'date': utils.now()
                }
                return models_dict[uuid]['model']

        else:
            print "KO"
            models_dict[uuid] = {'model': get_model(uuid), 'date': utils.now()}
            return models_dict[uuid]['model']

    return f


@cache_model
def get_model(uuid):
    """Given a uuid, it trains a ML model based on the
    datapoints saved so far"""
    schema = db.get_schema(uuid)
    features = schema['features']
    dataset = data_handling.datapoints_to_dataset(db.get_datapoints(uuid))
    train, target = data_handling.dataset_to_matrix(features, dataset)
    rf = ml.rf_factory()
    rf.fit(train, target)
    return rf


@service.route('/service/predict/<string:uuid>', methods=['POST'])
def predict(uuid):
    """Given a uuid and points
    {'points': [{'x1': .3, ..., 'xN': .7} ...]
    It returns a sequence of predictions
    {'results': [{mu: 1, sigma: .3}, ..., {mu: 2, sigma: .5}]}
    """
    schema = db.get_schema(uuid)
    data = flask.request.json
    if not data:
        flask.abort(400)  # bad request

    # TODO: optimize
    schema = db.get_schema(uuid)
    features = schema['features']
    points = data['points']
    vectors = data_handling.points_to_vectors(points, features)

    rf = get_model(uuid)
    mu, sigma = ml.random_forest_evaluate(rf, vectors)
    return json.dumps({'mu': list(mu), 'sigma': list(sigma)})


if __name__ == '__main__':
    service.run(port=settings.ml_service_port)
