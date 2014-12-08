import flask
import json

import settings
import db
import ml
import utils
import data_handling

service = flask.Flask(__name__)


def cache_model(seconds):
    """A decorator to cache the models"""

    def wrap(get_model):
        models_dict = {}

        def f(uuid, features):

            if (uuid in models_dict and
                'date' in models_dict[uuid] and
                'features' in models_dict[uuid] and
                (utils.now() - models_dict[uuid]['date']).seconds < seconds and
                models_dict[uuid]['features'] == features):
                return models_dict[uuid]['model']

            else:
                models_dict[uuid] = {
                    'model': get_model(uuid, features),
                    'date': utils.now(),
                    'features': features
                }
                return models_dict[uuid]['model']
        return f
    return wrap


@cache_model(5)
def get_model(uuid, features):
    """Given a uuid, it trains a ML model based on the
    datapoints saved so far"""
    dataset = data_handling.datapoints_to_dataset(db.get_datapoints(uuid))
    train, target = data_handling.dataset_to_matrix(features, dataset)
    rf = ml.rf_factory()
    rf.fit(train, target)
    return rf


@service.route('/service/feature-importances/<string:uuid>', methods=['GET'])
def feature_importances(uuid):
    """Given a uuid - It returns the feature importance
    {feature1: value1, feature2: value2, ...}"""
    schema = db.get_schema(uuid)
    features = schema['features']

    # Train/get a model on a given feature Set
    rf = get_model(uuid, features)
    feature_importances = rf.feature_importances_
    keys = sorted(features.keys())
    return json.dumps({key: feature_importances[i]
                       for i, key in enumerate(keys)})


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

    points = data['points']
    featureNamesFromPoints = set(data['points'][0].keys())

    schema = db.get_schema(uuid)
    features = schema['features']
    featureSet = set(features.keys())

    assert featureNamesFromPoints <= featureSet, \
        "some features are not defined in the schema: %s" \
        % str(featureNamesFromPoints - featureSet)

    # filters features that are in both points and the schema
    features = {f: features[f]
                for f in features
                if f in featureNamesFromPoints}

    # Train a model on a given feature Set
    rf = get_model(uuid, features)

    # Transform vectors on the same feature set
    vectors = data_handling.points_to_vectors(points, features)

    mu, sigma = ml.random_forest_evaluate(rf, vectors)
    return json.dumps({'mu': list(mu), 'sigma': list(sigma)})


if __name__ == '__main__':
    service.run(port=settings.ml_service_port)
