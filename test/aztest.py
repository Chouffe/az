import utils
import api
import db


def run_experiment(objective_function,
                   number_points_to_try,
                   number_trials,
                   number_binary_features,
                   features_to_show=[]):

    # Initialize the az testing
    az = api.AZTesting('aztest')
    az.delete()
    az = api.AZTesting('aztest')
    explored_points = []

    # Add the features
    for feature_name in ['a' + str(n)
                         for n in range(1, number_binary_features)]:
        # Only binary features for now
        az.add_feature(feature_name, 'binary')

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

    utils.format_results(explored_points,
                         number_trials,
                         number_binary_features,
                         sorted_points[0][1]['features'],
                         features_to_show)

# -------------------
# Set of experiments
# -------------------

run_experiment(utils.hyperplane_draw, 20, 200, 5)
# run_experiment(utils.obj_function_draw, 20, 200, 40, features_to_show=['a1', 'a2', 'a3'])
