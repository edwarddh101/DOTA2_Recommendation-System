'''
Pre-process the data from JSON file
    - Data Storage, MongoDB (Optional)
    - Pandas DataFrame
    - Save the DataFrame to csv
    - Build a psql database via csv files
'''

import json
import pandas as pd
import numpy as np
import pdb

class Data_process(object):
    '''
    Process the raw data JSON file and create two csv files for matches detail
    and players' information.
    '''
    def __init__(self,
                 raw_file='data_collection/match_history_t_part',
                 matches_csv='file/matches_csv',
                 players_csv='file/players_csv',
                 heroes_csv='file/heroes_csv_t',
                 human_players=10,
                 lobby_type=[0,7],
                 game_mode=[1,2,3,5,22]
                 ):
        self.raw_file = raw_file
        self.matches_csv=matches_csv
        self.players_csv=players_csv
        self.heroes_csv=heroes_csv
        self.human_players=human_players
        self.lobby_type=lobby_type
        self.game_mode=game_mode
        self.df=self.json_to_df()
        self.df_qualify=self.qualify_matches()

    def json_to_df(self):
        '''
        INPUT: JSON
        OUTPU: DataFrame
        '''
        match_json_array = []

        with open(self.raw_file) as f:
            for line in f:
                match_json_array.append(line)

        t = map(lambda x: pd.read_json(x), match_json_array)
        df = pd.concat(t,ignore_index=True)
        df = pd.DataFrame(df.matches.tolist())

        return df

    def qualify_matches(self):
        '''
        Criteria: 1. 10 human players
                  2. lobby_type: 0-CASUAL_MATCH
                                 7-COMPETITIVE_MATCH
                  3. Game_mode: 1-All pick
                                2-Captain Mode
                                3-Random Draft
                                4-Single Draft
                                5-All random
                                22-Ranked All Pick
                  4. Player time:
        '''
        df_qualify = self.df.copy()
        df_qualify = df_qualify[df_qualify['human_players']==self.human_players]
        df_qualify = df_qualify[df_qualify['lobby_type'].isin(self.lobby_type)]
        df_qualify = df_qualify[df_qualify['game_mode'].isin(self.game_mode)]

        return df_qualify

    def split_df(self):
        '''
        INPUT: None
        OUTPUT: data frame
        Split whole data frame to three data frames for match detail, players,
        and heroes.
        '''
        df_all = self.df_qualify.copy()
        df_players = df_all.pop('players')
        df_matches = df_all
        df_players_10 = pd.DataFrame(df_players.tolist(),index=df_players.index)
        df_heroes = df_players_10.applymap(lambda x: x['hero_id'])
        df_heroes = pd.concat([df_heroes,
                              df_matches[['radiant_win','match_id']]],
                              axis =1,
                              )

        return df_heroes, df_players, df_matches

    def main(self):
        '''
        Save data frame to three csv tables,  for hero list, match detail and
        players information.
        '''
        heroes = self.split_df()[0]
        heroes.to_csv(self.heroes_csv)

if __name__ == '__main__':
    data = Data_process()
    data.main()
