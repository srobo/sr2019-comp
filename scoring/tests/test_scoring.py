#!/usr/bin/env python

import unittest

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException

TEAMS_DATA =  {
    'ABC': {'zone': 0},  # green
    'DEF': {'zone': 1},  # orange
    'GHI': {'zone': 2},  # purple
}


class ScorerTests(unittest.TestCase):
    def construct_scorer(self, zone_contents):
        return Scorer(TEAMS_DATA, {'other': {'zone_contents': zone_contents}})

    def assertScores(self, expected_scores, zone_contents):
        scorer = self.construct_scorer(self.zone_contents)
        actual_scores = scorer.calculate_scores()

        self.assertEqual(expected_scores, actual_scores, "Wrong scores")

    def setUp(self):
        self.zone_contents = [
            [{'robots': [], 'tokens': ''} for _ in range(5)]
            for _ in range(5)
        ]

    def test_too_many_tokens_of_one_colour(self):
        # There are a total of 10 tokens of each colour
        self.zone_contents[0][0]['tokens'] = 'P' * 4
        self.zone_contents[0][1]['tokens'] = 'P' * 4
        self.zone_contents[1][1]['tokens'] = 'P' * 4

        scorer = self.construct_scorer(self.zone_contents)

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_invalid_token_colour(self):
        self.zone_contents[0][0]['tokens'] = 'Q'

        scorer = self.construct_scorer(self.zone_contents)

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_unexpected_robot(self):
        self.zone_contents[0][0]['robots'] = 'XYZ'

        scorer = self.construct_scorer(self.zone_contents)

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_single_token_on_base(self):
        self.zone_contents[0][0]['tokens'] = 'G'

        self.assertScores({
            'ABC': 2,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_single_token_on_volcano(self):
        self.zone_contents[1][1]['tokens'] = 'G'

        self.assertScores({
            'ABC': 7,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_single_token_in_caldera(self):
        self.zone_contents[2][2]['tokens'] = 'G'

        self.assertScores({
            'ABC': 30,
            'DEF': 0,
            'GHI': 0,
        }, self.zone_contents)

    def test_tied_zone(self):
        fail()

    def test_two_tied_zones(self):
        fail()

    def test_robot_on_base_affecting_zone_on_base(self):
        fail()

    def test_robot_on_volcano_affecting_zone_on_base(self):
        fail()

    def test_robot_on_volcano_affecting_zone_on_volcano(self):
        fail()

    def test_robot_on_volcano_affecting_zone_in_caldera(self):
        fail()

    def test_robot_in_caldera_affecting_zone_in_caldera(self):
        fail()

    def test_robot_in_zone_when_no_tokens(self):
        fail()

    def test_robot_in_zone_owned_by_other_team(self):
        fail()

    def test_robot_affects_zone_to_side(self):
        fail()

    def test_robot_doesnt_affect_zone_at_diagonal(self):
        fail()

    def test_robot_in_zone_affects_cardinal_points(self):
        # distribute owning of zones like so:
        # A B A
        # B R B
        # A B A
        # and check the resulting points for teams A and B
        # Note: maybe override the points for each type of
        # zone to be the same for this?
        fail()

    def test_two_robots_in_same_zone(self):
        fail()

    def test_two_robots_in_adjacent_zones(self):
        fail()

    def test_two_robots_in_diagonally_touching_zones(self):
        fail()


if __name__ == '__main__':
    unittest.main()
