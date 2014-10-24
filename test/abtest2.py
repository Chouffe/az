import utils
import api


def format_results(explored_points, number_trials, number_binary_features, best_point, features_to_show=[]):
    """Formats nicely the results of an experiment"""
    n = 0
    for i, p in enumerate(explored_points):
        if p == best_point:
            n = i
    print "-------------------------"
    print "Results of the Experiment"
    print "-------------------------"
    print
    print "Explored points: ", len(explored_points)
    print "Number trials: ", number_trials
    print "Number features: ", number_binary_features
    print
    print "Initial point: ", explored_points[0]
    for f in features_to_show:
        print f, ": ", explored_points[0][f]
    print "Best point: ", best_point
    for f in features_to_show:
        print f, ": ", best_point[f]
    print "Number of iterations: ", n
    print
    print "Path taken: "
    for p in explored_points:
        print p


def run_experiment(objective_function, number_points_to_try, number_trials, number_binary_features, features_to_show=[]):

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

    format_results(explored_points, number_trials,
                   number_binary_features, ab._current_baseline_point,
                   features_to_show)

# -------------------
# Set of experiments
# -------------------

# run_experiment(utils.hyperplane_draw, 20, 200, 10)
run_experiment(utils.obj_function_draw, 20, 200, 40, features_to_show=['a1', 'a2', 'a3'])
