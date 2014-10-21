from distributions import generate_random


def random_search(features):
    """Given a dict of the form feature -> {'distribution' 'params'}
    it returns a random point drawn from the distributions of each feature
    eg: random_search(
    {
        'a': {'distribution': 'normal', 'params': {'mu': 10, 'sigma': 3}},
        'c': {'distribution': 'uniform', 'params': {'low': 4, 'high': 5}},
        'd': {'distribution': 'binary', 'params': {}},
        'b': {'distribution': 'normal', 'params': {'mu': 1, 'sigma': .5}}
    })
    """
    return {k: generate_random(v['distribution'], v['params'], 1)[0]
            for k, v in features.iteritems()}
