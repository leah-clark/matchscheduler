import pandas as pd


def get_matches(data_set):
    if data_set == 1:
        return pd.read_pickle(r'testdata/matches3.pickle')
    return pd.read_pickle(r'testdata/matches2.pickle')


def get_squads(data_set):
    if data_set == 1:
        return pd.read_pickle(r'testdata/squads3.pickle')
    return pd.read_pickle(r'testdata/squads2.pickle')
