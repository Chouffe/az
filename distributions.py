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


class BinaryDistribution(Distribution):
    def generate(self, n=1):
        return np.random.randint(0, 2, n)


DISTRIBUTIONS = dict(
    normal=NormalDistribution,
    binary=BinaryDistribution,
    uniform=UniformDistribution
)


def generate_random(distribution_type, params, n):
    """Distribution type must be in DISTRIBUTIONS
    params: params for init the Distribution
    eg. mu, sigma, ...
    n: number of points to generate"""
    distribution = DISTRIBUTIONS[distribution_type](**params)
    return distribution.generate(n)
