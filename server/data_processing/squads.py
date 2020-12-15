import pandas as pd
from functools import reduce

def _get_table_by_condition(data_frame, column_name, specified_value):
    return data_frame.loc[data_frame[column_name] == specified_value]

def create_schedule_data(schedule):
    dfs = []

    squads = set(schedule['Squad'])

    for squad in squads:
        available_by_squad = _get_table_by_condition(schedule, 'Squad', squad)
        squad_data = []
        for row in available_by_squad.itertuples():
            if row.Shift == 'Night':
                squad_data.append([pd.to_datetime(row.Date + " " + "18:00"), row.Quantity*8])
            else:
                squad_data.append([pd.to_datetime(row.Date + " " + "10:00"), row.Quantity*8])

        dfs.append(pd.DataFrame(squad_data, columns=['Date', squad]))

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Date'],
                                                    how='outer'), dfs).fillna(0)

    df_merged['Total'] = df_merged[squads].sum(axis=1)
    df_merged_sorted = df_merged.sort_values(by=['Date'])
    df_merged_reset = df_merged_sorted.reset_index(drop=True)
    return df_merged_reset
