import os
import unittest
import pandas as pd
from datetime import datetime

from preferences import get_squad_preferences
from priority import schedule_days_matches

import test_helper


class TestGameScheduler(unittest.TestCase):

    def test_scheduler_data_set_1(self):
        # given
        shift_time = datetime(year=2019, month=4, day=16, hour=10, minute=0)
        squads_by_date = test_helper.get_squads(1)
        matches = test_helper.get_matches(1)
        preferences = get_squad_preferences(pd.read_csv("testdata/preferences.csv"))
        # when
        squad_letters = ['B+', 'E', 'D+', 'G', 'D', 'B', 'C', 'A']
        squads, left_over_matches = \
            schedule_days_matches(shift_time, matches, preferences, squads_by_date, squad_letters)
        output = []
        for squad in squads:
            if(squad.match_ids != []):
                for id in squad.match_ids:
                    output.append([squad.shift_time, squad.name, id])
        #then
        result = pd.DataFrame(output, columns=['Date', 'Squad', 'Game ID'])
        print(result)
        self.assertEqual(left_over_matches, [])
        self.assertEqual(result.loc[0]['Game ID'], 17055)
        self.assertEqual(result.loc[1]['Game ID'], 9623)
        self.assertEqual(result.loc[2]['Game ID'], 9255)
        self.assertEqual(result.loc[3]['Game ID'], 46684)
        self.assertEqual(result.loc[4]['Game ID'], 11813)
        self.assertEqual(result.loc[5]['Game ID'], 49819)
        self.assertEqual(result.loc[6]['Game ID'], 49820)
        self.assertEqual(result.loc[7]['Game ID'], 12681)
        self.assertEqual(result.loc[8]['Game ID'], 13110)


