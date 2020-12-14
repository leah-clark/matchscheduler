import os
from upload import save_to_server
from collectors import get_collector_hours_by_date
from squads import formats
from preferences import get_squad_preferences
from matches import formats
import pandas as pd

#todo: update endpoint on new alg
def process_csvs(game_data):
    save_to_server(game_data)
    schedule = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + '/schedule.csv')
    squads_by_date = formats(schedule)
    match_data = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + '/matches.csv')
    matches = formats(match_data)
    preferences = pd.read_csv(os.getcwd() + os.environ["DATA_PATH"] + "/preferences.csv")
    squad_preferences = get_squad_preferences(preferences)
    # object here?
    return squads_by_date, matches, squad_preferences
