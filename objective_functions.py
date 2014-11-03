import random
import utils
import numpy as np

# ----------------------------------
# Decorators to transform the signal
# ----------------------------------


def noisy(mu=0, sigma=1):
    def wrap(f):
        def g(*args, **kwargs):
            return f(*args, **kwargs) + utils.noise(mu=mu, sigma=sigma)
        return g
    return wrap


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

# ---------------------
# Objective functions
# ---------------------


def hyperplane(**kwargs):
    return float(sum(kwargs.values())) / len(kwargs)


@noisy(mu=0, sigma=.1)
def hyperplane_noisy(**kwargs):
    return hyperplane(**kwargs)


@draw
@noisy(mu=0, sigma=.1)
def hyperplane_noisy_draw(**kwargs):
    return hyperplane(**kwargs)


def obj_function1(a1, a2, a3, **kwargs):
    return float(a1 + a2 + a3) / 3


@draw
def obj_function1_draw(**kwargs):
    return obj_function1(**kwargs)


@noisy(mu=0, sigma=.1)
def obj_function1_noisy(**kwargs):
    return obj_function1(**kwargs)


def obj_function2(a1, **kwargs):
    return float(np.sinc(6 * (a1 - .5)))


@noisy(mu=0, sigma=.2)
def obj_function2_noisy(**kwargs):
    return obj_function2(**kwargs)
