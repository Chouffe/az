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


# TODO: add sequence of results. mean, std... foreach
# TODO: add best score
def format_results(explored_points, number_trials, number_binary_features,
                   best_point, features_to_show=[]):
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
