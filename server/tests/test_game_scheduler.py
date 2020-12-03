import os
import unittest
import pandas as pd
from datetime import datetime

from game_scheduler import schedule, calculate_interval, calculate_hours_per_interval

import test_helper


class TestGameScheduler(unittest.TestCase):

    def test_app(self):
        # given
        squads_by_date = test_helper.get_squads()
        matches = test_helper.get_matches()
        # when
        output = schedule(squads_by_date, matches)
        # then
        print(output)
        sut = output.loc[0]['Date']
        self.assertEqual(sut, 'hi')

    def test_calculate_interval(self):
        # given
        match_data = pd.read_csv("testdata/matches.csv")
        matches = format(match_data)
        datetime_schedule = datetime(year=2019, month=4, day=4, hour=18, minute=00)
        hours_per_interval = calculate_hours_per_interval(16)
        # when
        output = calculate_interval(16*8, hours_per_interval, 0, datetime_schedule, matches)
        # then
        self.assertEqual(output, 8)