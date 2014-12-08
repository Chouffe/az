import itertools

import api
import utils


def init_experiment(number_features,
                    uuid='abtest',
                    feature_names=[],
                    feature_distributions=[],
                    feature_params=[]):

    ab = api.ABTesting(uuid)

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
            ab.add_feature(feature_name, d, params=params)
        else:
            ab.add_feature(feature_name, d)

    return ab


def delete_experiment(uuid):
    ab = api.ABTesting(uuid)
    ab.delete()


def run_experiment(objective_function,
                   number_points_to_try,
                   number_trials,
                   number_features,
                   uuid='abtest',
                   feature_names=[],
                   feature_distributions=[],
                   feature_params=[]):

    delete_experiment(uuid)
    ab = init_experiment(number_features,
                         uuid=uuid,
                         feature_names=feature_names,
                         feature_distributions=feature_distributions,
                         feature_params=feature_params)
    explored_points = []
    max_try = 2

    # AB/Testing
    for _ in range(number_points_to_try):
        chosen = False
        k = 0

        while not chosen:
            if k >= max_try:
                break
            else:
                k += 1
                point_to_try = ab.get_candidate()

                if point_to_try not in explored_points:
                    chosen = True

        explored_points.append(point_to_try)
        for _ in range(number_trials):
            score = objective_function(**point_to_try)
            ab.save_result(point_to_try, score)

    datapoints = ab.datapoints
    best_point = ab._current_baseline_point
    best_score = utils.number_successes_trials_to_score(
        *ab._get_successes_and_trials(
            ab._current_baseline_point))

    return (explored_points,
            number_trials,
            number_features,
            datapoints,
            best_point,
            best_score)
