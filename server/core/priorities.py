import pandas as pd


class Priorities:

    def __init__(self):
        self.priorities = []

    def add(self, org_date):
        return org_date + self.priorities.pop()

    # todo: investigate pandas error thrown here
    def populate(self, competitions, finished_games):
        for game in finished_games.itertuples():
            self.priorities.append(pd.offsets.Hour(competitions[game.Competition]))
