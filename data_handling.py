import numpy as np
import utils
import db
import ml


def api_preprocess_datapoint(data):
    ddata = data.copy()
    result = ddata.pop('result')
    return result, ddata


def dataset_to_matrix(schema, dataset):
    """Given a schema and a dataset, it returns the
    training set and target set for the ml fitting
    eg.
    schema = {
        'a': {'default': 0},
        'b': {'default': 0},
        'c': {'default': 0}}
    dataset = [
        {'a': 0, 'b': 1, '_obj': 3.3},
        {'a': 1, 'b': 0, '_obj': 0.3},
        {'a': 1, 'b': 0, 'c': 1, '_obj': 7.3}]
    """
    keys = sorted(schema.keys())
    defaults = [schema[k]['default'] for k in keys]

    train = []
    target = []
    for point in dataset:
        row = []
        point_has_data = False
        for key, default in zip(keys, defaults):
            if key in point:
                point_has_data = True
                row.append(point[key])
            else:
                row.append(default)

        # ignoring data for old experiments,
        # should probably prune
        if point_has_data:
            train.append(row)
            target.append(point["_obj"])

    return np.array(train), np.array(target)


def datapoints_to_dataset(datapoints):
    """Given datapoints from the db, it returns the dataset
    {feature1: value1, ..., featureN: valueN, _obj: mu}"""
    point_dict = utils.process_datapoints(datapoints)
    return [dict(d['features'].items() + {'_obj': d['mu']}.items())
            for _, d in point_dict.items()]


# --------------------------------------
# Tests
# --------------------------------------

datapoints = db.get_datapoints('aztest')
features = db.get_schema('aztest')['features']
dataset = datapoints_to_dataset(db.get_datapoints('aztest'))
train, target = dataset_to_matrix(features, dataset)
random_points = np.array(ml.random_search(features, 10))


def point_to_vector(point, features):
    """Given a point {feature1: value1, ..., featureN: valueN}
    It returns [value1, ..., valueN] sorted by the keys"""
    return [point[key] for key in sorted(features.keys())]

print map(lambda p: point_to_vector(p, features), random_points)

print dataset
print features
print train, target

print ml.score_points(train,
                      target,
                      map(lambda p: point_to_vector(p, features),
                          random_points))
# TODO: keep only the N best ones
