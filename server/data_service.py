import os

from competitions import get_competition_priorities_kv_pair
from upload import save_to_server
from squads import create_schedule_data
from preferences import get_squad_preferences
from matches import create_match_data
import pandas as pd


def process_csvs(game_data):
    save_to_server(game_data)
    schedule = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + '/schedule.csv')
    squads_df = create_schedule_data(schedule)
    match_data = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + '/matches.csv')
    matches_df = create_match_data(match_data)
    preferences = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + "/preferences.csv")
    squad_preferences = get_squad_preferences(preferences)
    priorities_data = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + '/priorities.csv')
    competitions_data = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + "/competitions.csv")

    competitions = get_competition_priorities_kv_pair(priorities_data, competitions_data)
    return matches_df, squad_preferences, squads_df, competitions
