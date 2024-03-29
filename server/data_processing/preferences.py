from collections import defaultdict

'''
make a dictionary with {squad: preferred competition} pairing
eg.
{'B+': ['Ekstraklasa', 'La Liga']}
'''


def get_squad_preferences(preferences):
    squads_preferences = defaultdict(list)
    for row in preferences.itertuples():
        squads_preferences[row.Squad].append(row.Competition)
    return squads_preferences
