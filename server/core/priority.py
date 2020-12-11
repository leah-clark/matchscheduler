from datetime import datetime
import pandas as pd
from operator import attrgetter

from models.Squad import Squad


def populate_squads(available_squads, squad_letters, shift_time, squad_preferences):
    squads = []
    for letter in squad_letters:
        squad = Squad(name=letter, hours=available_squads[letter].values[0], shift_time=shift_time)
        squad.preferences = squad_preferences[letter]
        squads.append(squad)
        print(squad.name, squad.hours, squad.preferences)
    return squads

def find_squad_with_most_hours(squads):
    return max(squads, key=attrgetter('hours'))

def reassign_game(row, squads, carry_over_games):
    squad = find_squad_with_most_hours(squads)
    if squad.hours > 10:
        squad = add_match_to_schedule(10, squad, row.ID)
    else:
        print("This game will have to be carried over to tomorrow..")
        carry_over_games.append(row.ID)
    return squad, carry_over_games

def get_preferred_squad(squads, row):
    for squad in squads:
        if (row.Competition in squad.preferences):
            return squad
    return None

def add_match_to_schedule(time_taken, squad, match_id):
    squad.add_match_id(match_id)
    print("Match added to schedule... ")
    squad.hours -= time_taken
    return squad

def schedule_days_matches(shift_time, matches, preferences, squads_df, squad_letters):
    print("Shift is: " + str(shift_time))
    available_squads = squads_df.loc[squads_df['Date'] == shift_time]

    squads = populate_squads(available_squads,squad_letters,shift_time, preferences)

    carry_over_games = []
    # this searches in 'deadline' order
    for row in matches.itertuples():
        # get the squad that prefers this competition
        # assume 1 preference for 1 team for 1 competition
        squad = get_preferred_squad(squads, row)
        print("Competition: " + row.Competition)
        print(squad.hours)
        # if the squad is prefered - asign game
        if squad and squad.hours > 8:
            print("Squad: " + str(squad.name))
            print("Scheduling via preferece.. ")
            squad = add_match_to_schedule(8, squad, row.ID)
        # if not then give to squad wiht most availability
        else:
            print("Scheduling via size of squad.. ")
            squad, carry_over_games = reassign_game(row, squads, carry_over_games)
        # if any games left over - get put in next round, sorted in order
    return squads, carry_over_games

def schedule(matches, preferences, squads_df, squad_letters):
    match_schedule = []
    # this will get looped
    shift_time = datetime(year=2019, month=4, day=16, hour=10, minute=0)

    match_schedule, carry_over_games =\
        schedule_days_matches(shift_time, matches, preferences, squads_df, squad_letters)

    print(carry_over_games)

    return pd.DataFrame(match_schedule, columns=['Date', 'Squad', 'Game ID'])


