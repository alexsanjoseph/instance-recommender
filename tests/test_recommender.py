import pandas as pd
from instance_recommender.recommender import best_reco
from unittest import TestCase


class TestRecommender(TestCase):
    def test_case1(self):

        required_resources = {'vcpus': 17, 'memory': 26}

        instance_df = pd.DataFrame({
            'name': ['m5', 'c5', 'r5'],
            'vcpus': [2, 2, 2],
            'memory': [8, 4, 16],
            'price': [96, 85, 126]
        })

        actual = best_reco(required_resources, instance_df)

        expected = pd.DataFrame({
            'name': ['c5'],
            'units': 9.0,
            'vcpus': 2,
            'memory': 4,
            'price': 85
        })

        assert actual.equals(expected)

    def test_case2(self):

        required_resources = {'vcpus': 17, 'memory': 56}

        instance_df = pd.DataFrame({
            'name': ['m5', 'c5', 'r5'],
            'vcpus': [2, 2, 2],
            'memory': [8, 4, 16],
            'price': [96, 85, 126]
        })

        actual = best_reco(required_resources, instance_df)

        expected = pd.DataFrame({
            'name': ['m5', 'c5'],
            'units': [5.0, 4.0],
            'vcpus': [2, 2],
            'memory': [8, 4],
            'price': [96, 85]
        }).sort_values(['name']).reset_index(drop=True)

        assert actual.equals(expected)
