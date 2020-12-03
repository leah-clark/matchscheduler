import os
import unittest
import pandas as pd
from datetime import datetime

from collectors import get_collector_hours_by_date
from matches import format


class TestDataProcessing(unittest.TestCase):

    def test_collectors(self):
        # given
        schedules = pd.read_csv("testdata/schedule.csv")
        # when
        collector_hours_by_date = get_collector_hours_by_date(schedules)
        # then
        self.assertEqual(collector_hours_by_date.loc[0]['Collectors'], 31)
        self.assertEqual(collector_hours_by_date.loc[533]['Collectors'], 7)
        self.assertEqual(collector_hours_by_date.loc[45]['Collectors'], 20)
        self.assertEqual(collector_hours_by_date.loc[0]['Date'],
                         datetime(year=2019, month=3, day=31, hour=10, minute=0))
        self.assertEqual(collector_hours_by_date.loc[533]['Date'],
                         datetime(year=2019, month=5, day=1, hour=18, minute=0))
        self.assertEqual(collector_hours_by_date.loc[529]['Date'],
                         datetime(year=2019, month=4, day=29, hour=18, minute=0))

    def test_matches(self):
        # given
        match_data = pd.read_csv("testdata/matches.csv")
        # when
        matches = format(match_data)
        # then
        self.assertEqual(matches.loc[0]['Finish Date & Time'],
                         datetime(year=2019, month=4, day=1, hour=2, minute=20))
        self.assertEqual(matches.loc[1115]['Finish Date & Time'],
                         datetime(year=2019, month=4, day=30, hour=22, minute=35))
        self.assertEqual(matches.loc[50]['Counter'], 0)
