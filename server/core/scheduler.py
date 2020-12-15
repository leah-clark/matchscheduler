import pandas as pd

from game_handler import GameHandler, Priorities
from squad_handler import SquadHandler


def schedule_days_matches(shift_time, squad_handler, game_handler):
    # this searches in 'deadline' order
    game_handler.sort_games()
    for game in game_handler.games:
        # get the squad that prefers this competition
        # assume 1 preference for 1 team for 1 competition
        squad = squad_handler.get_preferred_squad(game)
        print("Competition: " + game.competition)

        if game.deadline < shift_time:
            time_late = shift_time - game.deadline
            print("Game " + str(game.game_id) + " is late by " + str(time_late))

        # if the squad is prefered - asign game
        if squad and squad.hours > 8:
            print("Squad: " + str(squad.name))
            print("Scheduling via preferece.. ")
            squad_handler.add_match_to_schedule(8, squad, game)

        # if not then give to squad wiht most availability
        else:
            print("Scheduling via size of squad.. ")
            squad_handler.reassign_game(game)
        # if any games left over - get put in next round, sorted in order
    unassigned_games = game_handler.filter_unassgined_games()
    return squad_handler.squads, unassigned_games


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


        # Sort by deadline so we have most urgent games being worked on first

        print("Shift is: " + str(row.Date))

        squads, unassigned_games = schedule_days_matches(row.Date, squad_handler, game_handler)

        match_schedule = sort_output(squads, match_schedule, row.Date)

    print("games not watched: ")
    for game in unassigned_games:
        print(game)
    print(len(unassigned_games))
    return pd.DataFrame(match_schedule, columns=['Date', 'Squad', 'Game ID'])
