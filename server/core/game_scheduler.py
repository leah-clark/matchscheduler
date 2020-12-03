from datetime import timedelta
from finished_games import get_finished_games
import pandas as pd

INTERVAL = 120

results = []

def calculate_hours_per_interval(number_of_collectors):
    return int(number_of_collectors / 60 * INTERVAL)


def calculate_game_hours_interval(datetime_schedule, matches):
    end_time = datetime_schedule + timedelta(minutes=INTERVAL)
    finished_games = get_finished_games(datetime_schedule, end_time, matches)
    return len(finished_games) * 8


def calculate_game_hours_completed(game_hours, hours_per_interval):
    game_hours -= hours_per_interval
    if game_hours < 0:
        game_hours = 0
    return game_hours


def calculate_interval(collectors_hours, hours_per_interval, game_hours, datetime_schedule, matches):
    if collectors_hours == 0:
        return game_hours
    results.append([datetime_schedule, game_hours, collectors_hours])
    # calculate game hours left here - using squads/priorities
    game_hours = calculate_game_hours_completed(game_hours, hours_per_interval)
    game_hours += calculate_game_hours_interval(datetime_schedule, matches)
    collectors_hours = collectors_hours - hours_per_interval
    return calculate_interval(collectors_hours, hours_per_interval, game_hours,
                              datetime_schedule + timedelta(minutes=INTERVAL), matches)


def calculate_game_hours_in_break(datetime_schedule, matches):
    if datetime_schedule.strftime('%H, %M') == "10, 00":
        finished_games = get_finished_games(
            datetime_schedule - timedelta(hours=8), datetime_schedule, matches)
        return len(finished_games) * 8
    return 0


def schedule(squads_by_date, matches, game_hours=0):
    for row in squads_by_date.itertuples():
        hours_per_interval = calculate_hours_per_interval(row.Total)
        game_hours += calculate_game_hours_in_break(row.Date, matches)
        game_hours = calculate_interval(
            row.Total * 8, hours_per_interval, game_hours, row.Date, matches)
    results_df = pd.DataFrame(results, columns=['Date', 'Game Hours', 'Collectors'])
    return results_df

