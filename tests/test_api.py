from nose import with_setup
import api
import itertools
import random
import db
import objective_functions
import data_handling

aztestname = 'test_api'


# Setup/Teardown


def setup_function():
    pass


def teardown_function():
    az = api.AZTesting(aztestname)
    az.delete()


def generate_aztest(n_features):
    az = api.AZTesting(aztestname)

    distributions = itertools.repeat('uniform')

    for feature_name, d in zip(['a' + str(n)
                                for n in range(1, n_features + 1)],
                               distributions):
        az.add_feature(feature_name, d)

    return az


@with_setup(setup_function, teardown_function)
def test_feature_addition():

    number_features = random.randint(1, 50)
    az = generate_aztest(number_features)

    assert len(az.features) == number_features


@with_setup(setup_function, teardown_function)
def test_feature_addition_in_db():

    number_features = random.randint(1, 50)
    generate_aztest(number_features)
    schema = db.get_schema(aztestname)
    assert len(schema['features'].keys()) == number_features


@with_setup(setup_function, teardown_function)
def test_deletion_features():

    az = generate_aztest(5)
    az.delete()
    schema = db.get_schema(aztestname)
    assert schema is None


@with_setup(setup_function, teardown_function)
def test_get_candidate():

    number_features = random.randint(1, 10)
    az = generate_aztest(number_features)
    point = az.get_candidate()
    assert len(point.keys()) == number_features


@with_setup(setup_function, teardown_function)
def test_get_candidate_after_adding_features():

    number_features = random.randint(1, 10)
    az = generate_aztest(number_features)
    point = az.get_candidate()
    az.add_feature('other-feature', 'normal')
    point = az.get_candidate()
    assert len(point.keys()) == number_features + 1


def add_points(az, n):
    for _ in range(n):
        point = az.get_candidate()
        value = objective_functions.hyperplane(**point)
        az.save_result(point, value)
    return az


@with_setup(setup_function, teardown_function)
def test_add_points():
    number_features = random.randint(1, 10)
    az = generate_aztest(number_features)
    number_points = random.randint(1, 10)
    add_points(az, number_points)

    assert len([p for p in db.get_datapoints(aztestname)]) == number_points


@with_setup(setup_function, teardown_function)
def test_get_graphs_results_after_adding_features():
    number_features = random.randint(1, 10)
    az = generate_aztest(number_features)
    number_points = random.randint(1, 10)
    add_points(az, number_points)

    az.add_feature('other-feature', 'uniform')
    schema = db.get_schema(aztestname)
    features = schema['features']
    datapoints = db.get_datapoints(aztestname)
    data = data_handling.datapoints_to_graph_results(datapoints, features)

    assert len(data) == number_features


@with_setup(setup_function, teardown_function)
def test_get_proj_results_after_adding_features():
    number_features = random.randint(1, 10)
    az = generate_aztest(number_features)
    number_points = random.randint(1, 10)
    add_points(az, number_points)

    az.add_feature('other-feature', 'uniform')
    schema = db.get_schema(aztestname)
    features = schema['features']
    datapoints = db.get_datapoints(aztestname)
    data = data_handling.datapoints_to_graph_results(datapoints, features)

    assert len(data) == number_features
