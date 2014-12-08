from nose import with_setup
import itertools
import random

import api
import data_handling
import db
import objective_functions


# Setup/Teardown
abtestname = 'test_api'

def setup_function():
    pass


def teardown_function():
    ab = api.ABTesting(abtestname)
    ab.delete()
    del(ab)


def generate_abtest(n_features):
    ab = api.ABTesting()
    distributions = itertools.repeat('binary')

    for feature_name, d in zip(['a' + str(n)
                                for n in range(1, n_features + 1)],
                               distributions):
        ab.add_feature(feature_name, d)
    return ab


@with_setup(setup_function, teardown_function)
def test_add_features():
    number_features = random.randint(1, 10)
    ab = generate_abtest(number_features)
    print ab.features
    assert len(ab.features) == number_features

#
# @with_setup(setup_function, teardown_function)
# def test_next_point():
#     number_features = random.randint(1, 10)
#     ab = generate_abtest(number_features)
#     point = ab.get_candidate()
#     print number_features
#     print point
#     assert len(point.keys()) == number_features
#
#
# def test_next_uniform_discrete_point():
#     number_features = random.randint(1, 10)
#     ab = api.ABTesting()
#     distributions = itertools.repeat('uniform_discrete')
#     params = {'low': 0, 'high': 10}
#
#     for feature_name, d in zip(['a' + str(n)
#                                 for n in range(1, number_features + 1)],
#                                distributions):
#         ab.add_feature(feature_name, d, params=params)
#
#     point = ab.get_candidate()
#     point = ab.get_candidate()
#     print point
#     assert len(point.keys()) == number_features

#
# def test_pick_feature_name():
#     ab = generate_abtest(5)
#     assert ab._pick_feature_name() in ab.features.keys()
#

# def test_pick_feature_name_with_explored_features():
#     ab = generate_abtest(5)
#     feature_names = ab.features.keys()
#     explored_feature_names = set(feature_names[:4])
#     ab._explored_feature_names = explored_feature_names
#     assert ab._pick_feature_name() not in explored_feature_names

#
# def test_generate_variation_feature_values():
#     ab = generate_abtest(5)
#     feature_names = ab.features.keys()
#     ab._current_variation_feature_name = feature_names[0]
#     assert len(ab._generate_variation_feature_values()) > 0
#     assert len(ab._current_variation_feature_values) > 0


# def test_get_next_point():
#     n_features = 5
#     ab = generate_abtest(n_features)
#     assert ab._current_baseline_point is None
#     assert ab._current_variation_point is None
#
#     baseline_point = ab.get_candidate()
#     variation_point = ab._generate_next_point(baseline_point)
#
#     assert ab._current_baseline_point is not None
#     assert ab._current_variation_point is None
#
#     assert len(baseline_point.keys()) == n_features
#     assert baseline_point != variation_point


# def test_get_candiadate():
#     n_features = 5
#     ab = generate_abtest(n_features)
#     assert ab._current_baseline_point is None
#     assert ab._current_variation_point is None
#
#     baseline_point = ab.get_candidate()
#     variation_point = ab.get_candidate()
#
#     assert ab._current_baseline_point is not None
#     assert ab._current_variation_point is not None
