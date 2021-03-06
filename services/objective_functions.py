import numpy as np
import random

import utils

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
        return int(rand < x)
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


# Black box optimization

def f_ramp(x0, y0=1, c0=1):
    # x0: where the max value is
    # y0: max value
    # c0: steeper
    def f(x):
        return max(0, y0 - np.abs(c0 * (x - x0)))
    return f


def obj_function_black_box1(a1, a2, **kwargs):

    # amplitude = 10
    # coeff = 1
    a10 = 5
    a20 = 3

    # norm = (a1 - a10)**2 + (a2 - a20)**2
    f1 = f_ramp(a10)
    f2 = f_ramp(a20)

    return (f1(a1) + f2(a2)) / 2


# Real world examples
def obj_function_landing_page(background,
                              font_size,
                              color,
                              number_columns,
                              popup,
                              **kwargs):
    """
    Variable meaning:
    -----------------
    - background: a categorical variable {0, 1, 2, ..., m}
    - font_size: a categorical variable {0, 1, ..., n}
    - color: a categorical variable {0, 1, ..., k}
    - number_columns: a categorical variable {0, 1, ..., l}
    - popup: a binary variable {0, 1} - is the popup displayed?
    """

    popup_f = f_ramp(1)
    background_f = f_ramp(2)
    font_size_f = f_ramp(5)
    color_f = f_ramp(3)
    number_columns_f = f_ramp(4)

    return float(6 * popup_f(popup)
                 + 3 * background_f(background)
                 + 3 * font_size_f(font_size)
                 + 2.5 * color_f(color)
                 + 1.5 * number_columns_f(number_columns)
                 ) / 120


@noisy(sigma=0.001)
def obj_function_landing_page_noisy(**kwargs):
    return obj_function_landing_page(**kwargs)


@draw
def obj_function_landing_page_draw(**kwargs):
    return obj_function_landing_page_noisy(**kwargs)
