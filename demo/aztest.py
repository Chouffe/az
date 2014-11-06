import utils
import api
import db
import itertools
import objective_functions
import experiments


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

# -------------------
# Set of experiments
# -------------------

# run_experiment(objective_functions.obj_function1_noisy,
#                100,
#                100,
#                10,
#                feature_distributions=itertools.repeat('uniform'))


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

# results = run_experiment(utils.obj_function_draw, 100, 200, 100, feature_distributions=itertools.repeat('uniform'))
# utils.format_results(*results, features_to_show=['a1', 'a2', 'a3'])

# Experiment 1 - Landing Page
# results = run_experiment(
#     objective_functions.obj_function_landing_page,
#     125,
#     100,
#     len(experiment_data['feature_names']),
#     uuid='lp',
#     feature_names=experiment_data['feature_names'],
#     feature_distributions=experiment_data['feature_distributions'],
#     feature_params=experiment_data['feature_params']
# )

# Experiment 1 - Landing Page
# results = experiments.run(experiments.landing_page, run_experiment)
# utils.format_results(*results)

# Experiment 2 - Landing Page 2
results = experiments.run(experiments.landing_page2, run_experiment)
utils.format_results(*results)
