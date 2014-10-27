import utils
import api


def run_experiment(objective_function,
                   number_points_to_try,
                   number_trials,
                   number_binary_features):

    # Initialize the ab testing
    ab = api.ABTesting()
    explored_points = []

    # Add the features
    for feature_name in ['a' + str(n)
                         for n in range(1, number_binary_features)]:
        # Only binary features for now
        ab.add_feature(feature_name, "binary")

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
            number_binary_features,
            datapoints,
            best_point,
            best_score)

# -------------------
# Set of experiments
# -------------------

# run_experiment(utils.hyperplane_draw, 20, 200, 10)
results = []
N = 10
for i in range(N):
    print "Running experiment #", i
    results.append(run_experiment(utils.obj_function_draw, 5, 200, 40))

utils.format_results(*results[0], features_to_show=['a1', 'a2', 'a3'])
utils.format_multiple_results(results)
