'''
Pre-process the data from JSON file
    - Data Storage, MongoDB (Optional)
    - Pandas DataFrame (Implement a Function)
    - Build a psql database (Implement a Function)
'''

import json
import pandas as pd
import numpy as np
import pdb

filename = 'data_collection/match_history_sample.json'

def json_to_df(file=filename, sample=0):
    '''
    INPUT: JSON
    OUTPU: DataFrame
    '''

    match_json_array = []
    if sample==0:
        with open(file) as f:
            for line in f:
                match_json_array.append(line)

    else:
        with open(file) as f:
            match_json_array = [next(f) for x in xrange(sample)]

    # pdb.set_trace()
    t = map(lambda x: pd.read_json(x), match_json_array)
    df = pd.concat(t,ignore_index=True)
    df = pd.DataFrame(df.matches.tolist())

    return df

def qualify_matches(df):
    return df[df['human_players']==10]

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
