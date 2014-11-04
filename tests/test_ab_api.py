import api
import itertools
import random
import db
import objective_functions
import data_handling


def generate_abtest(n_features):
    ab = api.ABTesting()
    distributions = itertools.repeat('binary')

    for feature_name, d in zip(['a' + str(n)
                                for n in range(1, n_features + 1)],
                               distributions):
        print "FEATURE", feature_name
        ab.add_feature(feature_name, d)

    return ab


# def test_add_features():
#     number_features = random.randint(1, 10)
#     ab = generate_abtest(number_features)
#     assert len(ab.features) == number_features

#
# def test_next_point():
#     number_features = random.randint(1, 10)
#     ab = generate_abtest(number_features)
#     point = ab.get_candidate()
#     print number_features
#     print point
#     assert len(point.keys()) == number_features


def test_next_uniform_discrete_point():
    number_features = random.randint(1, 10)
    ab = api.ABTesting()
    distributions = itertools.repeat('uniform_discrete')
    params = {'low': 0, 'high': 10}

    for feature_name, d in zip(['a' + str(n)
                                for n in range(1, number_features + 1)],
                               distributions):
        ab.add_feature(feature_name, d, params=params)

    point = ab.get_candidate()
    point = ab.get_candidate()
    print point
    assert len(point.keys()) == number_features
