import pandas as pd


def _add_finish_date_and_time(matches):
    matches['Match Date & Time'] = pd.to_datetime(matches['Match Date'] + " " + matches['Kick-off Time'],
                                                  format='%d/%m/%Y %H:%M')
    matches['Finish Date & Time'] = matches['Match Date & Time'] + pd.offsets.Minute(110)

def format(matches):
    _add_finish_date_and_time(matches)
    return matches
