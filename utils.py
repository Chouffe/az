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
