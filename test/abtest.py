import utils
import api
import objective_functions
import itertools


def init_experiment(number_features,
                    uuid='abtest',
                    feature_names=[],
                    feature_distributions=[],
                    feature_params=[]):

    ab = api.ABTesting()

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


def run_experiment(objective_function,
                   number_points_to_try,
                   number_trials,
                   number_features,
                   uuid='abtest',
                   feature_names=[],
                   feature_distributions=[],
                   feature_params=[]):

    # Initialize the ab testing
    ab = init_experiment(number_features,
                         uuid=uuid,
                         feature_names=feature_names,
                         feature_distributions=feature_distributions,
                         feature_params=feature_params)
    explored_points = []

    # AB/Testing
    for _ in range(number_points_to_try):
        point_to_try = ab.get_candidate()
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

# -------------------
# Set of experiments
# -------------------

# run_experiment(utils.hyperplane_draw, 20, 200, 10)
# results = []
# N = 1
# for i in range(N):
#     print "Running experiment #", i
#     results.append(run_experiment(utils.obj_function_draw, 50, 200, 40))
#
# utils.format_results(*results[0], features_to_show=['a1', 'a2', 'a3'])
# utils.format_multiple_results(results)
#
# Landing Page Experiment
experiment_data = {
    'objective_function': objective_functions.obj_function_landing_page,
    'feature_names': [
        "background",
        "font_size",
        "color",
        "number_columns",
        "popup"
    ],
    'feature_distributions': [
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "binary"
    ],
    'feature_params': [
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 15},
        {'low': 0, 'high': 6},
        {'low': 0, 'high': 10},
        {}
    ]
}

# Experiment 1 - Landing Page
results = run_experiment(
    objective_functions.obj_function_landing_page_draw,
    500,
    100,
    len(experiment_data['feature_names']),
    uuid='abtest',
    feature_names=experiment_data['feature_names'],
    feature_distributions=experiment_data['feature_distributions'],
    feature_params=experiment_data['feature_params']
)

utils.format_results(*results)
