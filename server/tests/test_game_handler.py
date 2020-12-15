import unittest
import pandas as pd
from datetime import datetime, timedelta

from competitions import get_competition_priorities_kv_pair
from matches import create_match_data
from game_handler import GameHandler
from priorities import Priorities


# todo: tests for SquadHandler
class TestGameHandler(unittest.TestCase):
    match_data = pd.read_csv("testdata/matches.csv")
    match_data = pd.read_csv("testdata/matches.csv")
    competition_data = pd.read_csv("testdata/competitions.csv")
    priorities_data = pd.read_csv("testdata/priorities.csv")

    def setup(self):
        matches = create_match_data(self.match_data)
        game_handler = GameHandler(matches_df=matches, priorities=None, competitions=None, games=[])
        return matches, game_handler

    def test_finished_games(self):
        # given
        matches, game_handler = self.setup()
        datetime_schedule = datetime(year=2019, month=4, day=1, hour=20, minute=50)
        end_time = datetime_schedule + timedelta(minutes=60)
        # when
        output = game_handler.get_finished_games(datetime_schedule, end_time)
        # then
        self.assertEqual(len(output), 4)
        self.assertEqual(output.loc[4]['ID'], 49811)

    def test_finished_games_before_ten(self):
        # given
        matches, game_handler = self.setup()
        datetime_schedule = datetime(year=2019, month=4, day=15, hour=10, minute=00)
        # when
        output = None
        if datetime_schedule.strftime('%H, %M') == "10, 00":
            output = game_handler.get_finished_games(
                datetime_schedule - timedelta(hours=8), datetime_schedule)
        # then
        self.assertEqual(len(output), 2)
        self.assertEqual(output.loc[520]['ID'], 46327)

    def test_sorting(self):
        competitions = get_competition_priorities_kv_pair(self.priorities_data, self.competition_data)
        matches, game_handler = self.setup()
        game_handler.competitions = competitions
        datetime_schedule = datetime(year=2019, month=4, day=15, hour=10, minute=00)
        # when
        game_handler.priorities = Priorities()
        game_handler.populate_games(datetime_schedule)
        game_handler.sort_games()
        # awful test but just a check to see if its all sorted manually
        for game in game_handler.games:
            print(game.deadline)
