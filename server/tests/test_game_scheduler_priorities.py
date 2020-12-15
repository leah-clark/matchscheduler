import unittest
import pandas as pd
from datetime import datetime

from game_handler import GameHandler
from priorities import Priorities
from preferences import get_squad_preferences
from scheduler import schedule_days_games, schedule, configure_output

from competitions import get_competition_priorities_kv_pair
from matches import create_match_data
from squad_handler import SquadHandler
from squads import create_schedule_data

import test_helper


class TestGameScheduler(unittest.TestCase):

    def test_sub_scheduler_data_set_1(self):
        # given
        shift_time = datetime(year=2019, month=4, day=16, hour=10, minute=0)
        squads_by_date = test_helper.get_squads()
        matches_df = test_helper.get_matches()
        competition_data = pd.read_csv("testdata/competitions.csv")
        priorities_data = pd.read_csv("testdata/priorities.csv")
        preferences = get_squad_preferences(pd.read_csv("testdata/preferences.csv"))
        competitions = get_competition_priorities_kv_pair(priorities_data, competition_data)
        game_handler = GameHandler(matches_df, Priorities(), competitions, [])
        game_handler.populate_games(shift_time)
        squad_handler = SquadHandler(squads_by_date)
        squad_handler.populate_squads(shift_time, preferences)
        # when
        squads, unassigned_games = \
            schedule_days_games(shift_time, squad_handler, game_handler)
        output = {}
        for squad in squads:
            output[squad.name] = set(squad.get_game_ids())
        #then
        print(output)
        self.assertEqual(unassigned_games, [])
        self.assertEqual(output['B+'], {49819, 13110})
        self.assertEqual(output['G'], {12681})
        self.assertEqual(output['C'], {11813, 17055})
        self.assertEqual(output['A'], {46684, 49820, 9255, 9623})



    def test_scheduler_data_set_1(self):
        # given
        competition_data = pd.read_csv("testdata/competitions.csv")
        priorities_data = pd.read_csv("testdata/priorities.csv")
        match_data = pd.read_csv("testdata/matches.csv")
        matches = create_match_data(match_data)
        squad_data = pd.read_csv("testdata/schedule.csv")
        squads = create_schedule_data(squad_data)
        preferences = get_squad_preferences(pd.read_csv("testdata/preferences.csv"))
        competitions = get_competition_priorities_kv_pair(priorities_data, competition_data)
        # when
        final_schedule, unassigned_games = schedule(matches, preferences, squads, competitions)

        # then all matches assigned are either scheduled or 'left over'
        self.assertEqual(final_schedule.shape[0] + unassigned_games.shape[0], match_data.shape[0])


