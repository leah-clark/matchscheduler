import os

from server.data_processing.competitions import get_competition_priorities_kv_pair
from server.upload import save_to_server
from server.data_processing.squads import create_schedule_data
from server.data_processing.preferences import get_squad_preferences
from server.data_processing.matches import create_match_data
import pandas as pd

# todo: pull out in env file
DATA_PATH = "/data/uploaded"


# process the cvs to a readable format for our algorithm
def process_csvs(game_data):
    save_to_server(game_data)
    schedule = pd.read_csv(os.getcwd() + DATA_PATH + '/schedule.csv')
    squads_df = create_schedule_data(schedule)
    match_data = pd.read_csv(os.getcwd() + DATA_PATH + '/matches.csv')
    matches_df = create_match_data(match_data)
    preferences = pd.read_csv(os.getcwd() + DATA_PATH + "/preferences.csv")
    squad_preferences = get_squad_preferences(preferences)
    priorities_data = pd.read_csv(os.getcwd() + DATA_PATH + '/priorities.csv')
    competitions_data = pd.read_csv(os.getcwd() + DATA_PATH + "/competitions.csv")

    competitions = get_competition_priorities_kv_pair(priorities_data, competitions_data)
    return matches_df, squad_preferences, squads_df, competitions
