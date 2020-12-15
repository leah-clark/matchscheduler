import pandas as pd

'''
creates table of matches, with the finish date & time added via average finishing time of 1 hour 20mins
eg.
ID	Match Date	Kick-off Time	Competition	Match Date & Time	Finish Date & Time
519	12681	15/04/2019	20:30	Serie A	2019-04-15 20:30:00	2019-04-15 22:20:00
'''


def _add_finish_date_and_time(matches):
    matches['Match Date & Time'] = pd.to_datetime(matches['Match Date'] + " " + matches['Kick-off Time'],
                                                  format='%d/%m/%Y %H:%M')
    matches['Finish Date & Time'] = matches['Match Date & Time'] + pd.offsets.Minute(110)


def create_match_data(matches):
    _add_finish_date_and_time(matches)
    return matches
