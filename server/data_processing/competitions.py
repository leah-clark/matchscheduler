'''
for each competition, find the priority in hours and add to a dictionary
eg.
{'Championship': 12}
as Championship is priority 1 = 12 hours
'''


def get_competition_priorities_kv_pair(priorities, competitions):
    priorities = priorities.set_index('Priority Class')
    pairs = {}
    for comp in competitions.itertuples():
        priority = comp.Priority
        # handle bad data
        if comp.Competition == 'Segunda División':
            pairs['Segunda DivisiÃ³n'] = priorities['Hours'][priority]
        else:
            pairs[comp.Competition] = priorities['Hours'][priority]

    return pairs
