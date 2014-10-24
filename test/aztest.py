import utils
import api
import db
import itertools


def run_experiment(objective_function,
                   number_points_to_try,
                   number_trials,
                   number_features,
                   feature_distributions=[]):

    # Initialize the az testing
    az = api.AZTesting('aztest')
    az.delete()
    az = api.AZTesting('aztest')
    explored_points = []

    # Default distributions: binary
    if not feature_distributions:
        feature_distributions = itertools.repeat('binary')

    # Add the features
    for feature_name, d in zip(['a' + str(n)
                                for n in range(1, number_features)],
                               feature_distributions):
        # Only binary features for now
        az.add_feature(feature_name, d)

    # AZ/ Testing
    for _ in range(number_points_to_try):
        point_to_try = az.get_candidate()
        explored_points.append(point_to_try)
        for _ in range(number_trials):
            score = objective_function(**point_to_try)
            az.save_result(point_to_try, score)

    # Get the best point so far
    datapoints = db.get_datapoints('aztest')
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

results = []
N = 100
for i in range(N):
    print "Running experiment #", i
    results.append(run_experiment(utils.obj_function_draw, 5, 200, 40))
# run_experiment(utils.hyperplane_draw, 16, 200, 5)
# results = run_experiment(utils.obj_function_draw, 100, 200, 100, feature_distributions=itertools.repeat('uniform'))
# utils.format_results(*results, features_to_show=['a1', 'a2', 'a3'])

# TODO: Save results somewhere
utils.format_multiple_results(results)
