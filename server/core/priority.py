from datetime import datetime
import pandas as pd

def get_squads_dic(available_squads, squad_letters):
    squads = {}
    for letter in squad_letters:
        squads[letter] = available_squads[letter].values[0]
    # so we don't have to check for null
    squads['null'] = 0
    return squads

def find_squad_with_most_hours(squads_dic):
    return max(squads_dic, key=lambda key: squads_dic[key])

def reassign_game(squads_dic, shift_time, row, match_schedule, carry_over_games):
    squad = find_squad_with_most_hours(squads_dic)
    if squads_dic[squad] > 10:
        squads_dic, match_schedule = add_match_to_schedule(10, match_schedule, shift_time, squad, row.ID, squads_dic)
    else:
        print("This game will have to be carried over to tomorrow..")
        carry_over_games.append(row.ID)
    return match_schedule, squads_dic, carry_over_games

def get_preferred_squad(preferences, row):
    squad_preference = preferences.loc[preferences['Competition'] == row.Competition]
    if( squad_preference.Squad.empty):
        return 'null'
    else:
        return squad_preference.Squad.values[0]

def remove_match_hours(time_taken, squads_dic, squad):
    print(squads_dic)
    squads_dic[squad] = squads_dic[squad] - time_taken
    print(str(time_taken)+" has been removed from squad "+ squad)
    print(squads_dic)
    return squads_dic

def add_match_to_schedule(time_taken, match_schedule, shift_time, squad, id, squads_dic):
    match_schedule.append([shift_time, squad, id])
    print("Match added to schedule... ")
    squads_dic = remove_match_hours(time_taken, squads_dic, squad)
    return squads_dic, match_schedule

def schedule_days_matches(shift_time, matches, preferences, squads, squad_letters, match_schedule):
    print("Shift is: " + str(shift_time))
    available_squads = squads.loc[squads['Date'] == shift_time]
    squads_dic = get_squads_dic(available_squads, squad_letters)
    carry_over_games = []
    # this searches in 'deadline' order
    for row in matches.itertuples():
        # get the squad that prefers this competition
        # assume 1 preference for 1 team for 1 competition
        squad = get_preferred_squad(preferences, row)
        print("Competition: " + row.Competition)
        print("Squad: " + squad)
        squad_hours = squads_dic[squad]
        # if the squad is prefered - asign game
        if squad_hours > 8:
            print("Scheduling via preferece.. ")
            squads_dic, match_schedule = add_match_to_schedule(8, match_schedule, shift_time, squad, row.ID, squads_dic)
        # if not then give to squad wiht most availability
        else:
            print("Scheduling via size of squad.. ")
            match_schedule, squads_dic, carry_over_games = \
                reassign_game(squads_dic, shift_time, row, match_schedule, carry_over_games)
        # if any games left over - get put in next round, sorted in order
    return match_schedule, carry_over_games

def schedule(matches, preferences, squads, squad_letters):
    match_schedule = []
    # this will get looped
    shift_time = datetime(year=2019, month=4, day=16, hour=10, minute=0)

    match_schedule, carry_over_games =\
        schedule_days_matches(shift_time, matches, preferences, squads, squad_letters, match_schedule)

    print(carry_over_games)

    return pd.DataFrame(match_schedule, columns=['Date', 'Squad', 'Game ID'])
