'''
Take JSON file and transfer it to pandas dataframe/
'''

import json
import pandas as pd
import numpy as np

filename = 'data_collection/match_history_sample.json'

def read_file(file=filename):
    '''
    INPUT: JSON
    OUTPU: DataFrame
    '''

    match_json_array = []
    with open(file) as f:
        for line in f:
            match_json_array.append(line)

    data=pd.DataFrame(match_json_array)
    t = map(lambda x: pd.read_json(x), match_json_array)
    df = pd.concat(t,ignore_index=True)
    df = pd.DataFrame(df.matches.tolist())

    return df

def match_features(players):
    vec = np.zeros(224, dtype=np.int)
    loc = np.append(np.zeros(5, dtype=np.int), np.ones(5, dtype=np.int)*112)
    loc+=map(lambda x: x['hero_id']-1, players)
    vec[loc]=1
    return vec

def matches_features(df):
    df_feature = df['players'].apply(lambda x: match_features(x))
    X = pd.DataFrame(df_feature.tolist())
    y = df['radiant_win']
    return X, y
