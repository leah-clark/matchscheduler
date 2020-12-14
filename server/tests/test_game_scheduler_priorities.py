import os
import unittest
import pandas as pd
from datetime import datetime

from preferences import get_squad_preferences
from scheduler import schedule_days_matches, schedule

from competitions import get_competition_priorities_kv_pair
from matches import formats
from squads import formats as ft

import test_helper


class TestGameScheduler(unittest.TestCase):

    def test_sub_scheduler_data_set_1(self):
        # given
        shift_time = datetime(year=2019, month=4, day=16, hour=10, minute=0)
        squads_by_date = test_helper.get_squads(1)
        matches = test_helper.get_matches(1)
        preferences = get_squad_preferences(pd.read_csv("testdata/preferences.csv"))
        # when
        squad_letters = ['B+', 'E', 'D+', 'G', 'D', 'B', 'C', 'A']
        squads, left_over_matches = \
            schedule_days_matches(shift_time, matches, preferences, squads_by_date, squad_letters)
        output = {}
        for squad in squads:
            output[squad.name] = set(squad.match_ids)
        #then
        print(output)
        self.assertEqual(left_over_matches, [])
        self.assertEqual(output['B+'], set([13110,49819]))
        self.assertEqual(output['G'], set([12681, 49820]))
        self.assertEqual(output['C'], set([11813, 17055]))
        self.assertEqual(output['A'], set([46684, 9255, 9623]))

    def test_scheduler_data_set_1(self):
        # given
        competition_data = pd.read_csv("testdata/competitions.csv")
        priorities = pd.read_csv("testdata/priorities.csv")
        match_data = pd.read_csv("testdata/matches.csv")
        matches = formats(match_data)
        squad_data = pd.read_csv("testdata/schedule.csv")
        squads = ft(squad_data)
        preferences = get_squad_preferences(pd.read_csv("testdata/preferences.csv"))
        competitions = get_competition_priorities_kv_pair(priorities, competition_data)
        # when
        squad_letters = ['B+', 'E', 'D+', 'G', 'D', 'B', 'C', 'A']
        final_schedule = schedule(matches, preferences, squads, squad_letters, competitions)
        print(final_schedule)

