import abc
import json
import random
import requests
from abba.stats import Experiment as ABExperiment

import db
import generator
import settings
import utils
from distributions import generate_random_from_feature
from distributions import get_default_params

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
base_url = "http://localhost:%s/api/" % settings.server_port
schema_url = base_url + "schema/"
feature_url = base_url + "feature/"


class ApiBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add_feature(self, feature_name, distribution, **kwargs):
        return

    @abc.abstractmethod
    def remove_feature(self, feature_name, **kwargs):
        return

    @abc.abstractmethod
    def get_candidate(self, **kwargs):
        return

    @abc.abstractmethod
    def save_result(self, point, result, **kwargs):
        return


class ABTesting(ApiBase):

    def __init__(self, uuid=None, baseline_point=None,
                 features={}, datapoints=[]):
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = utils.uuid()
        self.features = features
        # Dataset of tuples (point, result)
        self.datapoints = []

        # It keeps the baseline point and the variation point
        self._current_baseline_point = None
        self._current_variation_point = None

        self._explored_feature_names = set()
        self._current_variation_feature_name = None
        self._current_variation_feature_values = None

    def delete(self):
        """Deletes the entries in the DB"""
        db.delete_abdatapoints(self.uuid)

    def _generate_variation_feature_values(self):
        """When self._current_variation_feature_name is set,
        it samples some values to try"""
        assert self._current_baseline_point
        assert self._current_variation_feature_name

        rg = generator.RandomGenerator(self.features)
        random_values = set([rg.get_for_feature(
            self._current_variation_feature_name)[0]
            for _ in range(100)])

        baseline_value = self._current_baseline_point[
            self._current_variation_feature_name]
        if baseline_value in random_values:
            random_values.remove(baseline_value)

        self._current_variation_feature_values = list(random_values)
        random.shuffle(self._current_variation_feature_values)
        return self._current_variation_feature_values

    def add_feature(self, feature_name, distribution, **kwargs):
        """Given a feature name and a distribution, it adds a feature to
        the feature set"""
        self.features[feature_name] = {
            'distribution': distribution,
            'params': kwargs.get('params', get_default_params(distribution)),
            'default': kwargs.get('default', 0)
        }
        return self.features

    def remove_feature(self, feature_name, **kwargs):
        """Given a feature name, it removes the feature from the feature set"""
        return self.features.pop(feature_name)

    def _generate_random_point(self):
        """Generates a random point based on the features"""
        return {name: generate_random_from_feature(f)
                for name, f in self.features.iteritems()}

    def _pick_feature_name(self):
        """Randomly returns a feature name that has not been explored yet."""
        feature_names = self.features.keys()
        shuffled_feature_names = random.sample(feature_names,
                                               len(feature_names))
        selected_feature_name = None
        for f in shuffled_feature_names:
            if f not in self._explored_feature_names:
                selected_feature_name = f
                break

        return selected_feature_name

    def _generate_next_point(self, point):
        """Given a point, it generates the next one"""

        next_point = point.copy()
        assert len(self.features.keys()) > 0

        # If all the features have been explored
        if len(self._explored_feature_names) >= len(self.features.keys()):
            self._explored_feature_names = set()
            self._current_variation_feature_name = None
            self._current_variation_feature_values = []

        # If the feature values set is empty
        if not self._current_variation_feature_values:
            self._current_variation_feature_name = None

        # If no feature name is set
        if not self._current_variation_feature_name:
            self._current_variation_feature_name = self._pick_feature_name()
            self._generate_variation_feature_values()
            self._explored_feature_names.add(self._current_variation_feature_name)

        # Should be able to get a feature value
        assert len(self._current_variation_feature_values) > 0

        next_point[self._current_variation_feature_name] = self._current_variation_feature_values.pop()
        return next_point

    def _get_successes_and_trials(self, point):
        """Given a point, it returns the number of successes and
        trials stored in self.datapoints"""
        points = filter(lambda (p, r): p == point, self.datapoints)
        num_successes = len(filter(lambda (p, r): r > 0, points))
        return num_successes, len(points)

    def _ab_test(self, num_variations=1, confidence_level=0.95):
        """
        num_variations: number of different variations of experiment
        """
        baseline_num_successes, baseline_num_trials = self._get_successes_and_trials(self._current_baseline_point)
        num_successes, num_trials = self._get_successes_and_trials(
            self._current_variation_point)
        experiment = ABExperiment(num_variations,
                                  baseline_num_successes,
                                  baseline_num_trials,
                                  confidence_level)
        results = experiment.get_results(num_successes, num_trials)
        rel_improvement = results.relative_improvement
        p_value = results.two_tailed_p_value
        return p_value, rel_improvement.value

    def _is_ab_test_success(self):
        try:
            p_value, rel_improvement = self._ab_test()
            # Basic heuristic to keep the variation over the baseline
            return p_value <= .05 and rel_improvement > 0
        except ZeroDivisionError:
            return False

    def set_baseline(self, point):
        self._current_baseline_point = point

    def set_variation(self, point):
        self._current_variation_point = point

    def set_variation_feature(self, feature_name):
        self._current_variation_feature = feature_name

    def get_candidate(self, **kwargs):
        """Returns the candidate point to try next"""
        # if no baseline has been defined
        if not self._current_baseline_point:
            self._current_baseline_point = self._generate_random_point()
            return self._current_baseline_point
        # if no variation point has been defined
        elif not self._current_variation_point:
            self._current_variation_point = self._generate_next_point(self._current_baseline_point)
            return self._current_variation_point
        else:
            if self._is_ab_test_success():
                self._current_baseline_point = self._current_variation_point

            self._current_variation_point = self._generate_next_point(self._current_baseline_point)
            return self._current_variation_point

    def save_result(self, point, result, **kwargs):
        """Given a point + result, it saves it to a dataset"""
        self.datapoints.append((point, result))
        db.write_abdatapoint(self.uuid, point, result)
        return self.datapoints


class AZTesting(ApiBase):

    def __init__(self, uuid=None, features={}, datapoints=[]):
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = utils.uuid()
        self.features = features

        # Dataset of tuples (point, result)
        self.datapoints = []
        self._load_schema()

    def _load_schema(self):
        r = requests.get(schema_url + self.uuid)
        # If the schema exists
        if 'error' not in r.json():
            schema = r.json()
            if schema['features']:
                self.features = schema['features']
            return r.json()
        # Otherwise we create a new schema with no features
        else:
            r = requests.post(schema_url + self.uuid,
                              data=json.dumps({'features': {}}),
                              headers=headers)
            return self._load_schema()

    def delete(self):
        """Deletes the entries in the DB"""
        requests.delete(schema_url + self.uuid)

    def add_feature(self, feature_name, distribution, **kwargs):
        """Adds the feature name and the distribution in feature set"""
        feature_dict = {
            'distribution': distribution,
            'params': kwargs.get('params', get_default_params(distribution)),
            'default': kwargs.get('default', 0)
        }
        requests.post(feature_url + self.uuid,
                      data=json.dumps({feature_name: feature_dict}),
                      headers=headers)
        self.features[feature_name] = feature_dict
        return self.features

    def remove_feature(self, feature_name, **kwargs):
        """Removes the feature name of the feature set"""
        requests.delete(feature_url + self.uuid,
                        data=json.dumps({'feature_name': feature_name}),
                        headers=headers)
        self.features.pop(feature_name)
        return self.features

    def get_candidate(self, **kwargs):
        """Returns the next candidate to try"""
        r = requests.get(base_url + self.uuid)
        return r.json()

    def save_result(self, point, result, **kwargs):
        """Saves the point with its associated result"""
        self.datapoints.append((point, result))
        data = point.copy()
        data['result'] = result
        requests.post(base_url + self.uuid,
                      data=json.dumps(data),
                      headers=headers)
        return self.datapoints
