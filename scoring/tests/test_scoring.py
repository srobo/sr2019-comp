#!/usr/bin/env python

import unittest

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException


class ScorerTests(unittest.TestCase):
    def test_too_many_tokens_of_one_colour(self):
        fail()

    def test_invalid_token_colour(self):
        fail()

    def test_unexpected_robot(self):
        fail()

    def test_single_token_on_base(self):
        fail()

    def test_single_token_on_volcano(self):
        fail()

    def test_single_token_in_caldera(self):
        fail()

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
