import pandas as pd
import numpy as np
from datetime import timedelta
from models.Game import Game


class Priorities:

    def __init__(self):
        self.priorities = []

    def add(self, org_date):
        return org_date + self.priorities.pop()

    def populate(self, competitions, finished_games):
        for game in finished_games.itertuples():
            self.priorities.append(pd.offsets.Hour(competitions[game.Competition]))


class GameHandler:

    def __init__(self, matches, priorities, competitions, games):
        self.competitions = competitions
        self.matches = matches
        self.priorities = priorities
        self.games = games

    def populate_games(self, date):
        if date.strftime('%H, %M') == "10, 00":
            start_time = date - timedelta(hours=16)
        else:
            start_time = date - timedelta(hours=8)
        finished_games = self._get_finished_games(start_time, date)

        self.priorities.populate(self.competitions, finished_games)

        finished_games['Deadline'] = finished_games['Finish Date & Time'].apply(
            lambda org_date: self.priorities.add(org_date))
        # sometimes there are no games

        if (not finished_games.empty):
            for finished_game in finished_games.itertuples():
                game = Game(competition=finished_game.Competition, game_id=finished_game.ID, deadline=finished_game.Deadline)
                self.games.append(game)
        print(self.games)

    def _get_finished_games(self, starting_time, datetime_schedule):
        return self.matches.loc[np.logical_and(
            pd.to_datetime(self.matches['Finish Date & Time']) < datetime_schedule,
            pd.to_datetime(self.matches['Finish Date & Time']) >= starting_time)]

    def add_games(self, games, carry_over_ids):
        carry_over_games = self.matches[self.matches['ID'].isin(carry_over_ids)]
        return pd.concat([games, carry_over_games])

    def sort_games(self):
        self.games.sort(key=lambda x: x.deadline, reverse=True)

    def filter_unassgined_games(self):
        unassigned_games = []
        for game in self.games:
            if game.is_assigned == False:
                unassigned_games.append(game)
        return unassigned_games

