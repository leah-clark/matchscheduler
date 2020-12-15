import pandas as pd
import os
from game_handler import GameHandler
from priorities import Priorities
from squad_handler import SquadHandler


def schedule_days_games(shift_time, squad_handler, game_handler):
    # this searches in 'deadline' order
    game_handler.sort_games()
    for game in game_handler.games:
        #print(game.deadline)
        # get the squad that prefers this competition
        # assume 1 preference for 1 team for 1 competition
        squad = squad_handler.get_preferred_squad(game)
        #print("Competition: " + game.competition)

        if game.deadline < shift_time:
            time_late = shift_time - game.deadline
            print("Game " + str(game.game_id) + " is late by " + str(time_late))

        # if the squad is preferred - assign game
        if squad and squad.hours > 8:
            #print("Squad: " + str(squad.name))
            #print("Scheduling via preferece.. ")
            squad_handler.add_game_to_schedule(8, squad, game)

        # if not then give to squad with most availability
        else:
            #print("Scheduling via size of squad.. ")
            squad_handler.reassign_game(game)
    # if any games left over - get put in next round, sorted in order
    unassigned_games = game_handler.filter_unassigned_games()
    return squad_handler.squads, unassigned_games


def configure_output(squads, game_schedule, date):
    output = {}
    for squad in squads:
        output[squad.name] = set(squad.games)

    for key, value in output.items():
        for v in value:
            game_schedule.append([date, key, v.game_id])
    return game_schedule


def configure_unassigned_output(unassigned_games):
    game_ids = []
    deadlines = []
    for game in unassigned_games:
        game_ids.append(game.game_id)
        deadlines.append(game.deadline)
    return pd.DataFrame(data={"Game ID": game_ids, "Deadline": deadlines})


def schedule(matches_df, preferences, squads_df, competitions):
    games_schedule = []
    priorities = Priorities()
    unassigned_games = []
    # this loops over each shift pattern (10am, 6pm, 10am next day etc.)
    for row in squads_df.itertuples():
        game_handler = GameHandler(matches_df, priorities, competitions, unassigned_games)
        game_handler.populate_games(row.Date)
        squad_handler = SquadHandler(squads_df)
        squad_handler.populate_squads(row.Date, preferences)

        # Sort by deadline so we have most urgent games being worked on first

        #print("Shift is: " + str(row.Date))

        squads, unassigned_games = schedule_days_games(row.Date, squad_handler, game_handler)

        games_schedule = configure_output(squads, games_schedule, row.Date)

    unassigned_games_df = configure_unassigned_output(unassigned_games)
    schedule_df = pd.DataFrame(games_schedule, columns=['Date', 'Squad', 'Game ID'])

    return schedule_df, unassigned_games_df


def save_schedule(matches_df, preferences, squads_df, competitions):
    schedule_df, unassigned_games_df = schedule(matches_df, preferences, squads_df, competitions)
    # this would be stored somewhere on the server for production
    path = os.getcwd()
    schedule_df.to_csv(path + "/schedule.csv", index=False)
    unassigned_games_df.to_csv(path + "/unassigned.csv", index=False)
    return path
