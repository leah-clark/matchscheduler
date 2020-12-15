import unittest
import pandas as pd
from datetime import datetime

from server.core.game_handler import GameHandler
from server.core.priorities import Priorities
from server.core.squad_handler import SquadHandler
from server.core.scheduler import schedule_days_games, schedule

from server.data_processing.competitions import get_competition_priorities_kv_pair
from server.data_processing.matches import create_match_data
from server.data_processing.squads import create_schedule_data
from server.data_processing.preferences import get_squad_preferences

import test_helper


# integration testing
class TestGameScheduler(unittest.TestCase):
    competition_data = pd.read_csv("testdata/competitions.csv")
    priorities_data = pd.read_csv("testdata/priorities.csv")
    match_data = pd.read_csv("testdata/matches.csv")
    squad_data = pd.read_csv("testdata/schedule.csv")
    preferences = get_squad_preferences(pd.read_csv("testdata/preferences.csv"))

    def setup_integration(self):
        matches = create_match_data(self.match_data)
        squads = create_schedule_data(self.squad_data)
        competitions = get_competition_priorities_kv_pair(self.priorities_data, self.competition_data)
        return matches, squads, competitions

    def setup_handlers(self, shift_time):
        squads_by_date = test_helper.get_squads()
        matches_df = test_helper.get_matches()
        competitions = get_competition_priorities_kv_pair(self.priorities_data, self.competition_data)
        game_handler = GameHandler(matches_df, Priorities(), competitions, [])
        game_handler.populate_games(shift_time)
        squad_handler = SquadHandler(squads_by_date)
        squad_handler.populate_squads(shift_time, self.preferences)
        return squad_handler, game_handler

    def test_sub_scheduler_data_set_1(self):
        # given
        shift_time = datetime(year=2019, month=4, day=16, hour=10, minute=0)
        squad_handler, game_handler = self.setup_handlers(shift_time)
        # when
        squads, unassigned_games = \
            schedule_days_games(shift_time, squad_handler, game_handler)
        output = {}
        for squad in squads:
            output[squad.name] = set(squad.get_game_ids())
        # then
        self.assertEqual(unassigned_games, [])
        self.assertEqual(output['B+'], {49819, 13110})
        self.assertEqual(output['G'], {12681})
        self.assertEqual(output['C'], {11813, 17055})
        self.assertEqual(output['A'], {46684, 49820, 9255, 9623})

    def test_scheduler_data_set_1(self):
        # given
        matches, squads, competitions = self.setup_integration()
        # when
        final_schedule, unassigned_games = schedule(matches, self.preferences, squads, competitions)
        # then all matches assigned are either scheduled or 'left over'
        self.assertEqual(final_schedule.shape[0] + unassigned_games.shape[0], self.match_data.shape[0])
