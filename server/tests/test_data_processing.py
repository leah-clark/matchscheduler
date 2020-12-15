import os
import unittest
import pandas as pd
from datetime import datetime
from matches import create_match_data


# todo: tests for competitions, preferences and squads
class TestDataProcessing(unittest.TestCase):

    def test_matches(self):
        # given
        match_data = pd.read_csv("testdata/matches.csv")
        # when
        matches = create_match_data(match_data)
        # then
        self.assertEqual(matches.loc[0]['Finish Date & Time'],
                         datetime(year=2019, month=4, day=1, hour=2, minute=20))
        self.assertEqual(matches.loc[1115]['Finish Date & Time'],
                         datetime(year=2019, month=4, day=30, hour=22, minute=35))
