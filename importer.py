import json
import os
import urllib.request

import numpy as np
import pandas as pd

from config import API_URL, LOAD_FROM_API


def import_json_ms_data():
    if os.path.isfile('public.pickle'):
        print('file is present')
        df = pd.read_pickle('public.pickle')
    elif LOAD_FROM_API:
        full_json = []
        for i in range(0, 181):
            url_path = API_URL + "{0:03d}/".format(i)
            try:
                with urllib.request.urlopen(url_path) as url:
                    sample_json = json.loads(url.read().decode())
                    normalized_json = pd.json_normalize(sample_json, record_path='trajectories', meta='id')
                    if df is None:
                        df = normalized_json
                    else:
                        df = df.append(normalized_json, ignore_index=True)
                print(str(i) + ' is done!')
            except:
                print(str(i) + ' is invalid!')
        df.to_pickle('public.pickle')

    else:
        full_json = []
        for filename in os.listdir('Data/000/Trajectory/'):
            with open(os.path.join('Data/000/Trajectory/', filename), 'r') as f:  # open in readonly mode
                d = np.genfromtxt(os.path.join('Data/000/Trajectory/', filename), delimiter=',', skip_header=6,
                                  dtype=['float', 'float', 'int', 'int', 'float', 'datetime64[D]', 'object'],
                                  names=['lat', 'lon', 'x1', 'x2', 'altitude', 'date', 'time'])

                json_data = pd.DataFrame(d).to_dict(orient='records')
                full_json.append({
                    'id'          : '000',
                    'trajectories': json_data
                })

        for filename in os.listdir('Data/001/Trajectory/'):
            with open(os.path.join('Data/001/Trajectory/', filename), 'r') as f:  # open in readonly mode
                d = np.genfromtxt(os.path.join('Data/001/Trajectory/', filename), delimiter=',', skip_header=6,
                                  dtype=['float', 'float', 'int', 'int', 'float', 'datetime64[D]', 'object'],
                                  names=['lat', 'lon', 'x1', 'x2', 'altitude', 'date', 'time'])

                json_data = pd.DataFrame(d).to_dict(orient='records')
                full_json.append({
                    'id'          : '001',
                    'trajectories': json_data
                })

        df = pd.json_normalize(full_json, record_path='trajectories', meta='id')
        df.to_pickle('public.pickle')
