import datetime
import random
import numpy as np
from uuid import uuid1


def now():
    return datetime.datetime.utcnow()


def noise(mu=0, sigma=1):
    return np.random.normal(mu, sigma)


def to_int(v):
    try:
        return int(v)
    except:
        return 0


def uuid():
    return str(uuid1())

# ---------------------
#  Objective functions
# ---------------------


def draw(function):
    """Function domain has to be a subdomain of [0,1]
    It uniformely draws a value in 0, 1 and if x > draw its
    a success, otherwise its a failure"""
    def f(**kwargs):
        rand = random.random()
        x = function(**kwargs)
        if rand < x:
            # Success
            return 1
        else:
            # Failure
            return 0
    return f


def hyperplane(**kwargs):
    return float(sum(kwargs.values())) / len(kwargs)


@draw
def hyperplane_draw(**kwargs):
    return float(sum(kwargs.values())) / len(kwargs)


@draw
def obj_function_draw(a1, a2, a3, **kwargs):
    return float(a1 + a2 + a3) / 3

# ---------------------
#     Formatting
# ---------------------


def format_features_to_show(point, features_to_show):
    if features_to_show:
        print "Features: ", zip(features_to_show,
                                [point[f] for f in features_to_show])


def get_number_iterations_to_find_best_point(explored_points, best_point):
    for i, p in enumerate(explored_points):
        if p == best_point:
            return i
    # Raise an exception maybe?
    return -1


def format_results(explored_points,
                   number_trials,
                   number_features,
                   datapoints,
                   best_point,
                   best_score,
                   features_to_show=[]):
    """Formats nicely the results of an experiment"""
    n = get_number_iterations_to_find_best_point(explored_points, best_point)
    print "-------------------------"
    print "Results of the Experiment"
    print "-------------------------"
    print
    print "Explored points: ", len(explored_points)
    print "Number trials: ", number_trials
    print "Number features: ", number_features
    print
    print "Initial point: ", explored_points[0]
    format_features_to_show(explored_points[0], features_to_show)
    print
    print "Best point: ", best_point
    print "Score: ", best_score
    format_features_to_show(best_point, features_to_show)
    print
    print "Number of iterations to converge to the best point: ", n
    print
    print "Path taken: "
    for p in explored_points:
        print p


# TODO: add sequence of results. mean, std... foreach
def format_multiple_results(results, features_to_show=[]):
    """Given a sequence of results, it formats them
    results is a seq of
    - explored_points
    - number_trials
    - number_features
    - datapoints
    - best_point
    - best_score
    """
    best_score_array = np.array([])
    for r in results:
        print r
        print r[-1]
        best_score_array = np.append(best_score_array, r[-1])

    print "BEST SCORE ARRAY", best_score_array
    print "Best Score"
    print "Mean: ", best_score_array.mean()
    print "Std: ", best_score_array.std()

# ---------------------
# AB Testing processing
# ---------------------


def number_successes_trials_to_score(number_successes, number_trials):
    return float(number_successes) / number_trials


# ---------------------
#      DB utils
# ---------------------


def hash_datapoint(datapoint):
    """Given a point, it returns a hash of this point"""
    return hash(frozenset(datapoint['features'].items()))


# TODO: improve efficiency
def process_datapoints(datapoints):
    """Given datapoints, it processes them
    and return a dict
    - key: point hash
    - value: dict
        - mu: mean
        - sigma: standard deviation
        - n: number of datapoints
        - results: results obtained
        - features
    """
    point_dict = {}
    # Copy the datapoints
    ddata = [p for p in datapoints]
    for point in ddata:
        point_dict[hash_datapoint(point)] = {'results': [],
                                             'features': point['features']}

    for point in ddata:
        point_dict[hash_datapoint(point)]['results'].append(point['result'])

    for e in point_dict:
        result_array = np.array(point_dict[e]['results'])
        point_dict[e]['n'] = len(point_dict[e]['results'])
        point_dict[e]['mu'] = np.mean(result_array)
        point_dict[e]['sigma'] = np.std(result_array)
        del point_dict[e]['results']

    return point_dict


def sort_point_dict(point_dict):
    """Given a point_dict, it sorts them. Sorts only by  mean for now"""
    return sorted(list(point_dict.items()),
                  key=lambda (h, d): d['mu'],
                  reverse=True)
