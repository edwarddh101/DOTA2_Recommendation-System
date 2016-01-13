'''
This is the module for heroes recommendation based on winnig rate
'''

import pickle
import numpy as np
import pandas as pd
# import pdb


class Heroes_recommend(object):
    def __init__(self,
                 file='file/model_sample.pkl',
                 file_heroes='file/hero_id_list.csv',
                 max_hero_id=113,
                 current_radiant_heroes=[1, 2],
                 current_dire_heroes=[28, 99],
                 invalid_heroes_id=[24, 108, 113],
                 home_team='radiant'):
        self.file = file
        self.model = self.load_model()
        self.file_heroes = file_heroes
        self.current_radiant_heroes = current_radiant_heroes
        self.current_dire_heroes = current_dire_heroes
        self.max_hero_id = max_hero_id
        self.invalid_heroes_id = invalid_heroes_id
        self.home_team = home_team
        self.heroes_pool = self.heroes_pool()

    def heroes_pool(self):
        '''
        INPUT:
        OUTPUT: Array
        Extract current heroes id
        '''
        df = pd.read_csv(self.file_heroes)
        heroes_pool = np.array(df['id'])[:-1]
        return heroes_pool

    def load_model(self):
        '''
        load the best trained model
        '''
        with open(self.file) as f:
            model = pickle.load(f)
        return model

    def rad_dir(self, heroes_num):
        '''
        Transform the roaster to radiant and dire format
        '''
        return np.array([0]*heroes_num+[113]*heroes_num)

    def transform(self):
        '''
        transform the input heroes to feature matrix,
        Exclude the heroes have already choose
        '''
        x = np.zeros(self.max_hero_id*2)
        available_heroes = np.copy(self.heroes_pool)
        for hero_id in self.current_radiant_heroes:
            x[hero_id - 1] = 1
            available_heroes = available_heroes[available_heroes != hero_id]
        for hero_id in self.current_dire_heroes:
            x[hero_id - 1 + self.max_hero_id] = 1
            available_heroes = available_heroes[available_heroes != hero_id]
        return x, available_heroes

    def x_valid(self, x):
        '''
        delete the invalid features
        '''
        invalid_heroes = self.invalid_heroes_id * 2 + \
            self.rad_dir(len(self.invalid_heroes_id))
        return np.delete(x, invalid_heroes - 1)

    def hero_candidates(self):
        '''
        Rank hero candiates based on winning rate
        '''
        x, available_heroes = self.transform()
        candidates_prob = []
        if self.home_team == 'radiant':
            for hero_candidate in available_heroes:
                # pdb.set_trace()
                x[hero_candidate - 1] = 1
                prob = self.model.predict_proba(self.x_valid(x))
                candidates_prob.append((prob[0][1], hero_candidate))
        else:
            for hero_candidate in available_heroes:
                x[hero_candidate - 1 + self.max_hero_id] = 1
                prob = self.model.predict_proba(self.x_valid(x))
                candidates_prob.append((prob[0][0], hero_candidate))
        return sorted(candidates_prob, reverse=True)

    def best_heroes(self):
        '''
        recommend heroes based on given information
        '''
        candidates_prob = self.hero_candidates()
        if self.home_team == 'radiant':
            i = len(self.current_radiant_heroes)
            return candidates_prob[:5 - i]
        else:
            j = len(self.current_dire_heroes)
            return candidates_prob[:5 - j]

    def main(self):
        with open('file/best_heroes_demo', 'a') as f:
            f.write('radiant: {0}, dire: {1}, {2}: {3}'
                    .format(self.current_radiant_heroes,
                            self.current_dire_heroes,
                            self.home_team,
                            self.best_heroes()))

if __name__ == '__main__':
    best_heroes = Heroes_recommend()
    best_heroes.main()
