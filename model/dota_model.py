""" Class for model training and storage. Procedures:
    1. Generate Feature matrixes from database/csv file
    2. Model training_logistic and random forest
    3. Performance comparison_ROC curve and accuracy
    prediction on test data
    4. Store the model
"""

import numpy as np
import ast
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import pickle


class Dota2_model(object):
    def __init__(self,
                 file='file/heroes_csv_sample',
                 max_hero_id=113,
                 invalid_heroes_id=[24, 108, 113]
                 ):
        self.file = file
        self.max_hero_id = max_hero_id
        self.invalid_heroes_id = invalid_heroes_id
        self.classifiers = [
                LogisticRegression(C=1),
                RandomForestClassifier(n_estimators=10000,
                                       n_jobs=-1,
                                       min_samples_leaf=50,
                                       random_state=50),
                AdaBoostClassifier()]

    def rad_dir(self, heroes_num):
        '''
        Transform the roaster to radiant and dire format
        '''
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
        invalid_heroes = self.invalid_heroes_id * 2 + \
            self.rad_dir(len(self.invalid_heroes_id))
        x = np.delete(x, invalid_heroes - 1)
        return x, y

    def csv_transform(self):
        '''
        Extract features from raw file
        '''
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
        '''
        Split the dataset to training and testing dataset
        '''
        X, y = self.csv_transform()
        return cross_validation.train_test_split(X, y, test_size=0.8)

    def model_training(self):
        '''
        Use trainin dataset to train the models
        '''
        X_train, X_test, y_train, y_test = self.train_test_split()
        classifiers_trained = []
        auc_score = []
        y_scores = []
        for classifier in self.classifiers:
            clf = classifier
            clf.fit(X_train, y_train)
            classifiers_trained.append(clf)
            y_score = clf.predict_proba(X_test)[:, 1]
            auc_score.append(roc_auc_score(y_test, y_score))
            y_scores.append(y_score)
        return classifiers_trained, y_scores, auc_score

    def roc_fig(self):
        '''
        Plot the roc_curve for candidate models
        '''
        classifiers, y_scores, auc_score = self.model_training()
        X_train, X_test, y_train, y_test = self.train_test_split()
        fpr_tpr = []
        plt.figure(num=None, figsize=(12, 9), dpi=800,
                   facecolor='w', edgecolor='k')
        plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
        for i in range(len(classifiers)):
            fpr_tpr.append(roc_curve(y_test, y_scores[i])[:-1])
            if i == 0:
                plt.plot(fpr_tpr[i][0], fpr_tpr[i][1],
                         '-', c='r', lw=1,
                         label='Logistic ROC (area = %0.2f)'
                         % auc_score[i])
            if i == 1:
                plt.plot(fpr_tpr[i][0], fpr_tpr[i][1],
                         'k--', lw=1,
                         label='RandomForest ROC (area = %0.2f)'
                         % auc_score[i])
            if i == 2:
                plt.plot(fpr_tpr[i][0], fpr_tpr[i][1],
                         '-.', lw=1,
                         label='AdaBoosting ROC (area = %0.2f)'
                         % auc_score[i])

        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic_model comparison')
        plt.legend(loc="lower right")
        plt.savefig('file/roc_curve_model_comparison')

    def main(self):
        '''
        compare the models and store the best model in the pickle.
        '''
        classifiers_trained, _, auc_score = self.model_training()
        best_ix = np.argsort(auc_score)[-1]
        best_model = classifiers_trained[best_ix]
        with open('file/model.pkl', 'w') as f:
            pickle.dump(best_model, f)

if __name__ == '__main__':
    dota2_model = Dota2_model()
    dota2_model.main()
    dota2_model.roc_fig()
