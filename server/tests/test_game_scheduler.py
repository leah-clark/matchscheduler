import os
import unittest
import pandas as pd
from datetime import datetime

from game_scheduler import schedule, calculate_interval, calculate_hours_per_interval

import test_helper


class TestGameScheduler(unittest.TestCase):

    def test_scheduler_data_set_1(self):
        # given
        squads_by_date = test_helper.get_squads(1)
        matches = test_helper.get_matches(1)
        # when
        output = schedule(squads_by_date, matches)
        print(output)
        # then
        hours_test = output.loc[15]['Game Hours']
        collectors_test = output.loc[20]['Collectors']
        self.assertEqual(hours_test, 24)
        self.assertEqual(collectors_test, 184)

    def test_scheduler_data_set_2(self):
        # given
        squads_by_date = test_helper.get_squads(2)
        matches = test_helper.get_matches(2)
        # when
        output = schedule(squads_by_date, matches)
        # then
        print(output)
        hours_test = output.loc[4]['Game Hours']
        collectors_test = output.loc[10]['Collectors']
        print(collectors_test)
        self.assertEqual(hours_test, 172)
        self.assertEqual(collectors_test, 64)

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