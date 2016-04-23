import datetime
import pandas as pd
import requests

BASE_URL = 'http://oe1.orf.at/programm/konsole/tag/'

DEFAULT_COLUMNS = ['time', 'title', 'info']

def get_oe1_program(day='20160423', offline=False):
    if offline:
        return _get_oe1_program_offline()
    url = BASE_URL + day
    response = requests.get(url, stream=True)
    return pd.DataFrame(response.json()['list'])

def _get_oe1_program_offline():
    return pd.DataFrame.from_csv('offline.csv', encoding='utf-8')

def _get_date_from_row(row):
    return datetime.datetime.strptime(row['day_label'] + row['time'], '%d.%m.%Y%H:%M')

def post_process_program(program):
    program = program.set_index('id')
    program['datetime'] = program.apply(_get_date_from_row, axis=1)
    return program

def filter_program(program, columns=None):
    if not columns:
        columns = DEFAULT_COLUMNS
    return program.loc[:,columns]

def print_program(program):
    program.columns = [c.title() for c in program.columns]
    print program.to_string(index=False).encode('utf-8')

print_program(filter_program(post_process_program(get_oe1_program(offline=True))))
