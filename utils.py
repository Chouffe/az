import datetime
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
