from datetime import datetime, timedelta
import pandas as pd
from operator import attrgetter

from finished_games import get_finished_games

from models.Squad import Squad


def populate_squads(available_squads, squad_letters, shift_time, squad_preferences):
    squads = []
    for letter in squad_letters:
        squad = Squad(name=letter, hours=available_squads[letter].values[0], shift_time=shift_time)
        squad.preferences = squad_preferences[letter]
        squads.append(squad)
    return squads


def find_squad_with_most_hours(squads):
    return max(squads, key=attrgetter('hours'))


def reassign_game(row, squads, carry_over_ids):
    squad = find_squad_with_most_hours(squads)
    print("Squad: " + str(squad.name))
    if squad.hours > 10:
        squad = add_match_to_schedule(10, squad, row.ID)
    else:
        print("This game will have to be carried over to tomorrow..")
        carry_over_ids.append(row.ID)
    return squad, carry_over_ids


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


def schedule_days_matches(shift_time, matches, preferences, available_squads, squad_letters):
    squads = populate_squads(available_squads, squad_letters, shift_time, preferences)
    carry_over_ids = []
    # this searches in 'deadline' order
    for row in matches.itertuples():
        # get the squad that prefers this competition
        # assume 1 preference for 1 team for 1 competition
        squad = get_preferred_squad(squads, row)
        print("Competition: " + row.Competition)

        if row.Deadline < shift_time:
            print("Late game!")

        # if the squad is prefered - asign game
        if squad and squad.hours > 8:
            print("Squad: " + str(squad.name))
            print("Scheduling via preferece.. ")
            squad = add_match_to_schedule(8, squad, row.ID)
        # if not then give to squad wiht most availability
        else:
            print("Scheduling via size of squad.. ")
            squad, carry_over_ids = reassign_game(row, squads, carry_over_ids)
        # if any games left over - get put in next round, sorted in order
    return squads, carry_over_ids


def add_priority_hours(org_date, priorities):
    return org_date + priorities.pop()


def calculate_priority_hours(competitions, finished_games):
    priorities = []
    for game in finished_games.itertuples():
        priorities.append(pd.offsets.Hour(competitions[game.Competition]))
    return priorities


def get_games(row, competitions, matches):
    end_time = row.Date
    if end_time.strftime('%H, %M') == "10, 00":
        start_time = end_time - timedelta(hours=16)
    else:
        start_time = end_time - timedelta(hours=8)
    # when
    finished_games = get_finished_games(start_time, end_time, matches)

    priorities = calculate_priority_hours(competitions, finished_games)

    finished_games['Deadline'] = finished_games['Finish Date & Time'].apply(
        lambda org_date: add_priority_hours(org_date, priorities))

    return finished_games


def add_games(games, carry_over_ids, matches):
    carry_over_games = matches[matches['ID'].isin(carry_over_ids)]
    return pd.concat([games, carry_over_games])


def sort_output(squads, match_schedule, date):
    output = {}
    for squad in squads:
        output[squad.name] = set(squad.match_ids)

    for key, value in output.items():
        for v in value:
            match_schedule.append([date, key, v])
    return match_schedule


def schedule(matches, preferences, squads_df, squad_letters, competitions):
    match_schedule = []
    carry_over_ids = []
    # this will get looped
    for row in squads_df.itertuples():
        games = get_games(row, competitions, matches)
        games_plus_carryover = add_games(games, carry_over_ids, matches)
        games_plus_carryover_sorted = games_plus_carryover.sort_values('Deadline')

        print("Shift is: " + str(row.Date))
        # change to row
        available_squads = squads_df.loc[squads_df['Date'] == row.Date]

        squads, carry_over_ids = schedule_days_matches(
            row.Date, games_plus_carryover_sorted, preferences, available_squads, squad_letters)

        match_schedule = sort_output(squads, match_schedule, row.Date)

    return pd.DataFrame(match_schedule, columns=['Date', 'Squad', 'Game ID'])
