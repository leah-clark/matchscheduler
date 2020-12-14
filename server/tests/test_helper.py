import pandas as pd


def get_matches():
    return pd.read_pickle(r'tests/testdata/matches.pickle')


def get_squads():
    return pd.read_pickle(r'tests/testdata/squads.pickle')
