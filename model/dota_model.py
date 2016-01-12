'''Class for model training and storage. Procedures:
    1. Generate Feature matrixes from database/csv file
    2. Model training_logistic and random forest
    3. Performance comparison_ROC curve and accuracy
    prediction on test data
    4. Store the model
'''

import numpy as np
import ast
# import pandas as pd
from sklearn import cross_validation
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.grid_search import GridSearchCV


class Dota2_model(object):
    def __init__(self,
                 file='file/heroes_csv_sample',
                 max_hero_id=113,
                 invalid_heroes_id=[24, 108, 113]
                 ):
        self.file = file
        self.max_hero_id = max_hero_id
        self.invalid_heroes_id = invalid_heroes_id

    def rad_dir(self, heroes_num):
        return np.array([0]*heroes_num+[113]*heroes_num)

    def transform(self, line):
        '''
        INPUT: one lien of CSV file
        OUTPUT: Feature matrixes
        '''
        x = np.zeros(self.max_hero_id*2)
        data = line.split(',')[1:-1]
        y = ast.literal_eval(data[-1])
        x_raw = map(int, data[:-1])
        rad_dir = self.rad_dir(5)
        x_raw = x_raw + rad_dir
        for id in x_raw:
            x[id] = 1
        invalid_heroes = self.invalid_heroes_id * 2 \
                       + self.rad_dir(len(self.invalid_heroes_id))
        x = np.delete(x, invalid_heroes - 1)
        return x, y

    def csv_transform(self):
        X = []
        y = []
        with open(self.file) as f:
            next(f)
            for line in f:
                _x, _y = self.transform(line)
                X.append(_x)
                y.append(_y)
        return X, y

    def train_test_split(self):
        X, y = self.csv_transform()
        return cross_validation.train_test_split(X, y, test_size=0.8)

    def model_training(self):
        '''
        '''
        X_train, X_test, y_train, y_test = self.train_test_split()
        pass

    def roc_curve():
        '''
        '''
        pass

# if __name__==__main__:
#     pass
