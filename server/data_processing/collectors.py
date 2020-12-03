import pandas as pd

def _get_table_by_condition(data_frame, column_name, specified_value):
    return data_frame.loc[data_frame[column_name] == specified_value]

def _get_shift_by_date(schedule):
    data = []
    for date in schedule['Date']:
        available_by_date = _get_table_by_condition(schedule, 'Date', date)
        night_shift = _get_table_by_condition(available_by_date, 'Shift', 'Night')
        morning_shift = _get_table_by_condition(available_by_date, 'Shift', 'Morning')
        data.append([date, night_shift['Quantity'].sum(), morning_shift['Quantity'].sum()])

    return pd.DataFrame(data, columns=['Date', 'Night', 'Morning'])

def _get_morn_night_tables(shift_by_date):
    date_morn = shift_by_date[['Date', 'Morning']]
    date_morn = date_morn.rename(columns={"Morning": "Collectors"})
    date_morn['Date'] = pd.to_datetime(date_morn['Date'] + " " + "10:00")
    date_night = shift_by_date[['Date', 'Night']]
    date_night = date_night.rename(columns={"Night": "Collectors"})
    date_night['Date'] = pd.to_datetime(date_night['Date'] + " " + "18:00")
    return date_morn, date_night

def get_collector_hours_by_date(schedule):
    shift_by_date = _get_shift_by_date(schedule)
    date_morn, date_night = _get_morn_night_tables(shift_by_date)
    return pd.concat([date_morn, date_night]).sort_index(kind="mergesort").reset_index(drop=True)