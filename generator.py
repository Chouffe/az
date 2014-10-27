import abc
from distributions import DISTRIBUTIONS


class Generator(object):
    """Interface for the generators"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self, **kwargs):
        """Returns n points generated by the generator"""
        pass


class RandomGenerator(Generator):
    """Random Generator"""

    def __init__(self, features):
        """
        features
        {
            'a': {'distribution': 'normal', 'params': {'mu': 10, 'sigma': 3}},
            'c': {'distribution': 'uniform', 'params': {'low': 4, 'high': 5}},
            'd': {'distribution': 'binary', 'params': {}},
            'b': {'distribution': 'normal', 'params': {'mu': 1, 'sigma': .5}}
        })"""
        self.features = features

    def get(self, n=1):
        """Randomly generates n points based on the distributions
        of the features"""
        points = []
        for _ in xrange(n):
            point = dict()
            for k, v in self.features.iteritems():
                distribution = DISTRIBUTIONS[v['distribution']](**v['params'])
                point[k] = distribution.generate(1)[0]
            points.append(point)
        return points


# Example
# r = RandomGenerator({
#         'a': {'distribution': 'normal', 'params': {'mu': 10, 'sigma': 3}},
#         'c': {'distribution': 'uniform', 'params': {'low': 4, 'high': 5}},
#         'd': {'distribution': 'binary', 'params': {}},
#         'b': {'distribution': 'normal', 'params': {'mu': 1, 'sigma': .5}}
#     })
#
# print r.get()
