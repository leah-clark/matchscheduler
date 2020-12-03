import os
import unittest
import pandas as pd
from datetime import datetime, timedelta

from matches import format
from finished_games import get_finished_games


class TestFinishedGames(unittest.TestCase):

    # integration
    def test_finished_games(self):
        # given
        match_data = pd.read_csv("testdata/matches.csv")
        matches = format(match_data)
        datetime_schedule = datetime(year=2019, month=4, day=1, hour=20, minute=50)
        end_time = datetime_schedule + timedelta(minutes=60)
        # when
        output = get_finished_games(datetime_schedule, end_time, matches)
        print(output)
        # then
        self.assertEqual(len(output), 4)
        self.assertEqual(output.loc[4]['ID'], 49811)

    def test_finished_games_before_ten(self):
        # given
        match_data = pd.read_csv("testdata/matches.csv")
        matches = format(match_data)
        datetime_schedule = datetime(year=2019, month=4, day=15, hour=10, minute=00)
        # when
        output = None
        if datetime_schedule.strftime('%H, %M') == "10, 00":
            output = get_finished_games(
                datetime_schedule - timedelta(hours=8), datetime_schedule, matches)
        # then
        print(output)
        self.assertEqual(len(output), 4)
        self.assertEqual(output.loc[0]['ID'], 46330)

    def test_update_matches(self):
        return 'true'
