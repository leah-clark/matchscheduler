import pandas as pd
import numpy as np


def get_finished_games(starting_time, datetime_schedule, matches):
    return matches.loc[np.logical_and(
        pd.to_datetime(matches['Finish Date & Time']) < datetime_schedule,
        pd.to_datetime(matches['Finish Date & Time']) >= starting_time)]
