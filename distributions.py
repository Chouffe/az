import numpy as np
import abc


class Distribution(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self, n):
        return


class NormalDistribution(Distribution):
    def __init__(self, mu=0, sigma=1):
        self.mu = mu
        self.sigma = sigma

    def generate(self, n=1):
        return np.random.normal(self.mu, self.sigma, n)


class UniformDistribution(Distribution):
    def __init__(self, low=0, high=1):
        self.low = low
        self.high = high

    def generate(self, n=1):
        return np.random.uniform(self.low, self.high, n)


class UniformDiscreteDistribution(Distribution):
    def __init__(self, low=0, high=1):
        self.low = low
        self.high = high

    def generate(self, n=1):
        return np.random.randint(self.low, self.high, n)


class BinaryDistribution(Distribution):
    def generate(self, n=1):
        return np.random.randint(0, 2, n)


DISTRIBUTIONS = dict(
    binary=BinaryDistribution,
    normal=NormalDistribution,
    uniform_discrete=UniformDiscreteDistribution,
    uniform=UniformDistribution
)


def get_default_params(distribution):
    if distribution == 'binary':
        return {}
    elif distribution == 'normal':
        return {'mu': 0, 'sigma': 1}
    elif distribution == 'uniform':
        return {'low': 0, 'high': 1}
    elif distribution == 'uniform_discrete':
        return {'low': 0, 'high': 1}
    else:
        return {}


def generate_random(distribution_type, params, n):
    """Distribution type must be in DISTRIBUTIONS
    params: params for init the Distribution
    eg. mu, sigma, low, high, ...
    n: number of points to generate"""
    distribution = DISTRIBUTIONS[distribution_type](**params)
    return distribution.generate(n)


def generate_random_from_feature(feature):
    return generate_random(feature['distribution'], feature['params'], 1)[0]
