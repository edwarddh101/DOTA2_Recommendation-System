import pandas as pd
import numpy as np
from sklearn import cross_validation, linear_model
from sklearn.ensemble import RandomForestClassifier


# def match_features(players):
#     vec = np.zeros(224, dtype=np.int)
#     loc = np.append(np.zeros(5, dtype=np.int), np.ones(5, dtype=np.int)*112)
#     loc+=map(lambda x: x['hero_id']-1, players)
#     vec[loc]=1
#     return vec
#
# def matches_features(df):
#     df_player_features = df['players'].apply(lambda x: match_features(x))
#     X = pd.DataFrame(df_player_features.tolist())
#     y = df['radiant_win']
#     return X, y

def model_lg(df):
    X, y = matches_features(df)
    clf_log_r = linear_model.LogisticRegression()
    print "model_lg CV: {0}".format(
            cross_validation.cross_val_score(clf_log_r, X, y, cv=5))

def model_rf(df):
    X, y = matches_features(df)
    clf_rf = RandomForestClassifier()
    print "model_rf CV score: {0}".format(
            cross_validation.cross_val_score(clf_rf, X, y, cv=5))

if __name__ == '__main__':
    model_lg()
    model_rf()
