import numpy as np
import utils
import db
import ml


def api_preprocess_datapoint(data):
    ddata = data.copy()
    result = ddata.pop('result')
    return result, ddata


# TODO: Test it
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


def datapoints_to_graph_results(datapoints, features):
    point_dict = utils.process_datapoints(datapoints)
    tmp = [dict(m['features'].items() +
                {'time': sorted(m['time'])[-1]}.items())
           for _, m in point_dict.items()]
    tmp = sorted(tmp, key=lambda d: d['time'])
    results = {f: [] for f in features}

    for e in tmp:
        for f in features:
            if f in e:
                results[f].append(e[f])
            else:
                results[f].append(features[f]['default'])

    return results


def point_to_vector(point, features):
    """Given a point {feature1: value1, ..., featureN: valueN}
    It returns [value1, ..., valueN] sorted by the keys"""
    return [point[key] for key in sorted(features.keys())]


def points_to_vectors(points, features):
    return map(lambda p: point_to_vector(p, features), points)


def vector_to_point(vector, features):
    """Given a vector [value1, ..., valueN]
    It returns {feature1: value1, ..., featureN: valueN}"""
    return {key: vector[i] for i, key
            in enumerate(sorted(features.keys()))}
