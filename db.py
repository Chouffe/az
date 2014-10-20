# ---------------
#    DB Schema
# ---------------
# schemas
# - uuid
#   eg: "experiment1"
# - features
#   Sequence of
#   - feature-name -> {"default", "distribution", "params"}
#     - default: default value
#     - distribution: "gaussian", "uniform", "poisson", ...
#     - params: params required for the distribution
#   eg [{"btn-color" {"default": 0,
#                     "distribution": "normal",
#                     "params": {"mu": 0, "sigma" 2.2}}]
# datapoints
# - uuid: schema uuid
# - time: Date of when it was created
# - features
#   {"btn-color" 0, "font-size" 12 ...}
# - result: result of the objective function
#   eg: 12.3


import settings
from pymongo import MongoClient


def init_db():
    """Initializes the db connection and returns the default
    db connection instance"""
    client = MongoClient()
    return client[settings.db_name]
