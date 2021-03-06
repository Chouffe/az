# ---------------
#    DB Schema
# ---------------
#
# - schemas: Keeps the schemas of the tests
#   - uuid
#     eg: "experiment1"
#   - features
#     Dict of
#     - feature-name -> {"default", "distribution", "params"}
#       - default: default value
#       - distribution: in #{"normal", "uniform", "uniform_discrete", "binary"}
#       - params: params required for the distribution
#                 mu, sigma, low, high
#     eg [{"btn-color" {"default": 0,
#                       "distribution": "normal",
#                       "params": {"mu": 0, "sigma" 2.2}}]
#
# - datapoints: Keeps the datapoints of the tests
#   - uuid: schema uuid
#   - time: Date of when it was created
#   - features
#     {"btn-color" 0, "font-size" 12 ...}
#   - result: result of the objective function
#     eg: 12.3

# - abdatapoints: Keeps the datapoints of the A/B tests
#   - uuid: schema uuid
#   - time: Date of when it was created
#   - features
#     {"btn-color" 0, "font-size" 12 ...}
#   - result: result of the A/B test: 0 or 1

from pymongo import MongoClient

import distributions
import settings
import utils


def init_db():
    """Initializes the db connection and returns the default
    db connection instance"""
    client = MongoClient()
    return client[settings.db_name]

# db contains the db connection
db = init_db()


def create_indexes():
    """Initializes the indexes on the collections"""
    db['schemas'].ensure_index('uuid', unique=True)
    db['datapoints'].ensure_index('uuid')


def drop_inndexes():
    """Drops all the indexes"""
    db['schemas'].drop_indexes()
    db['datapoints'].drop_indexes()

# -----------------------
#       Schemas
# -----------------------


def write_schema(uuid, features):
    """Given an uuid and a sequence of features,
    it writes the schema in the db"""
    data = {'uuid': uuid, 'features': features}
    return db['schemas'].insert(data)


def get_schema(uuid):
    """Given an uuid, it returns the schema of this uuid"""
    return db['schemas'].find_one({'uuid': uuid})


def get_schemas():
    """Given an uuid, it returns the schema of this uuid"""
    return [s for s in db['schemas'].find({})]


def delete_schema(uuid):
    """Given an uuid, it deletes the schema associated to this uuid"""
    return db['schemas'].remove({'uuid': uuid})

# -----------------------
#       Features
# -----------------------


def add_feature(uuid, feature):
    """Given an uuid and a feature, it adds the feature to the schema"""
    schema = get_schema(uuid)

    feature_dict = feature.items()[0][1]
    distribution = feature_dict['distribution']

    if not feature_dict['params']:
        feature_dict['params'] = distributions.get_default_params(distribution)

    if not feature_dict['default']:
        feature_dict['default'] = 0

    new_feature_set = dict(schema['features'].items() + feature.items())
    return db['schemas'].update({'uuid': uuid},
                                {"$set": {"features": new_feature_set}})


def remove_feature(uuid, feature_name):
    """Given an uuid and a feature, it adds the feature to the schema"""
    schema = get_schema(uuid)
    new_feature_set = schema['features']
    new_feature_set.pop(feature_name, None)
    return db['schemas'].update({'uuid': uuid},
                                {"$set": {"features": new_feature_set}})


# -----------------------
#       Datapoints
# -----------------------

def write_datapoint(uuid, features, result):
    """Given an uuid and a sequence of features, it writes
    the point in the db"""
    data = {'uuid': uuid,
            'features': features,
            'result': result,
            'time': utils.now()}
    return db['datapoints'].insert(data)


def delete_datapoints(uuid):
    """Given an uuid it deletes all the datapoints"""
    return db['datapoints'].remove({'uuid': uuid})


def get_datapoints(uuid):
    """Given an uuid it returns all the datapoints associated with it"""
    return db['datapoints'].find({'uuid': uuid})


# -----------------------
#      AB Datapoints
# -----------------------

def write_abdatapoint(uuid, features, result):
    """Given an uuid and a sequence of features, it writes
    the point in the db"""
    data = {'uuid': uuid,
            'features': features,
            'result': result,
            'time': utils.now()}
    return db['abdatapoints'].insert(data)


def delete_abdatapoints(uuid):
    """Given an uuid it deletes all the datapoints"""
    return db['abdatapoints'].remove({'uuid': uuid})


def get_abdatapoints(uuid):
    """Given an uuid it returns all the datapoints associated with it"""
    return db['abdatapoints'].find({'uuid': uuid})
