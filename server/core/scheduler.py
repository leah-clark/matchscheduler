import pandas as pd

from game_handler import GameHandler, Priorities
from squad_handler import SquadHandler

class Scheduler:
    def __init__(self, squad_scheduler, game_scheduler):
        self.game_scheduler = game_scheduler
        self.squad_scheduler = squad_scheduler

    def add_match_to_schedule(self, time_taken, squad, game):
        squad.add_match_id(game)
        print("Match added to schedule... ")
        squad.hours -= time_taken
        game.assign_game(squad)

    def reassign_game(self, game):
        squad = self.squad_handler.find_squad_with_most_hours()
        print("Squad: " + str(squad.name))
        if squad.hours > 10:
            self.add_match_to_schedule(10, squad, game)
            game.assign_game(squad)
        else:
            print("This game will have to be carried over to tomorrow..")

    def get_preferred_squad(self, game):
        return self.squad_handler.get_preferred_squad(game)

    def sort_games(self):
        self.game_scheduler.sort_games()

    def filter_unassgined_games(self):
        return self.squad_scheduler()

    def get_squads(self):
        return self.squad_scheduler.squads

def schedule_days_matches(shift_time, scheduler):
    # this searches in 'deadline' order
    games = scheduler.sort_games()
    unassigned_games = []
    if games:
        for game in scheduler.sort_games():
            # get the squad that prefers this competition
            # assume 1 preference for 1 team for 1 competition
            squad = scheduler.get_preferred_squad(game)
            print("Competition: " + game.Competition)

            if game.Deadline < shift_time:
                time_late = shift_time - game.Deadline
                print("Game " + str(game.ID) + " is late by " + str(time_late))

            # if the squad is prefered - asign game
            if squad and squad.hours > 8:
                print("Squad: " + str(squad.name))
                print("Scheduling via preferece.. ")
                scheduler.add_match_to_schedule(8, squad, game)

            # if not then give to squad wiht most availability
            else:
                print("Scheduling via size of squad.. ")
                scheduler.reassign_game(game)
            # if any games left over - get put in next round, sorted in order
            unassigned_games = scheduler.filter_unassgined_games()
    return scheduler.get_squads(), unassigned_games


def sort_output(squads, match_schedule, date):
    output = {}
    for squad in squads:
        output[squad.name] = set(squad.match_ids)

    for key, value in output.items():
        for v in value:
            match_schedule.append([date, key, v])
    return match_schedule


def schedule(matches_df, preferences, squads_df, competitions):
    match_schedule = []
    priorities = Priorities()
    unassigned_games = []
    # this will get looped
    for row in squads_df.itertuples():
        game_handler = GameHandler(matches_df, priorities, competitions, unassigned_games)
        game_handler.populate_games(row.Date)
        squad_handler = SquadHandler(squads_df)
        squad_handler.populate_squads(row.Date, preferences)

        scheduler = Scheduler(squad_handler, game_handler)

        # Sort by deadline so we have most urgent games being worked on first

        print("Shift is: " + str(row.Date))

        squads, unassigned_games = schedule_days_matches(row.Date, scheduler)

        match_schedule = sort_output(squads, match_schedule, row.Date)

    print("games not watched: ")
    for game in unassigned_games:
        print(game)
    return pd.DataFrame(match_schedule, columns=['Date', 'Squad', 'Game ID'])
