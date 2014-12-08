import itertools

import api
import db
import utils


def init_experiment(number_features,
                    uuid='aztest',
                    feature_names=[],
                    feature_distributions=[],
                    feature_params=[]):

    az = api.AZTesting(uuid)

    # Default distributions: binary
    if not feature_distributions:
        feature_distributions = itertools.repeat('binary')

    if not feature_names:
        feature_names = ['a' + str(n) for n in range(1, number_features + 1)]

    if not feature_params:
        feature_params = itertools.repeat(None)

    # Add the features
    for feature_name, d, params in zip(feature_names,
                                       feature_distributions,
                                       feature_params):
        if params:
            az.add_feature(feature_name, d, params=params)
        else:
            az.add_feature(feature_name, d)

    return az


def delete_experiment(uuid):
    az = api.AZTesting(uuid)
    az.delete()


def run_experiment(objective_function,
                   number_points_to_try,
                   number_trials,
                   number_features,
                   uuid='aztest',
                   feature_names=[],
                   feature_distributions=[],
                   feature_params=[]):

    delete_experiment(uuid)
    az = init_experiment(number_features,
                         uuid=uuid,
                         feature_names=feature_names,
                         feature_distributions=feature_distributions,
                         feature_params=feature_params)

    explored_points = []

    # AZ/ Testing
    for _ in range(number_points_to_try):
        # time.sleep(2)
        point_to_try = az.get_candidate()
        explored_points.append(point_to_try)
        for _ in range(number_trials):
            score = objective_function(**point_to_try)
            az.save_result(point_to_try, score)

    # Get the best point so far
    datapoints = db.get_datapoints(uuid)
    point_dict = utils.process_datapoints(datapoints)
    sorted_points = utils.sort_point_dict(point_dict)

    best_point = sorted_points[0][1]['features']
    best_score = sorted_points[0][1]['mu']
    datapoints = az.datapoints

    return (explored_points,
            number_trials,
            number_features,
            datapoints,
            best_point,
            best_score)
