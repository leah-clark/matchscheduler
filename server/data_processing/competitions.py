
def get_competition_priorities_kv_pair(priorities, competitions):
    priorities = priorities.set_index('Priority Class')
    priorities['Hours'][1]
    pairs = {}
    for comp in competitions.itertuples():
        priority = comp.Priority
        print(comp.Competition)
        if (comp.Competition == 'Segunda División'):
            pairs['Segunda DivisiÃ³n'] = priorities['Hours'][priority]
        else:
            pairs[comp.Competition] = priorities['Hours'][priority]

    return pairs