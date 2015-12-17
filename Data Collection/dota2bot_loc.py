import os #, logging, argparse
import dota2api
# from util import get_game_mode_string
from pymongo import MongoClient
from time import sleep
from sys import exit
import datetime


#connect to mongo db
mongo_client=MongoClient()
db = mongo_client.dota2
coll = db.match_history


#set up dota2api

api = dota2api.Initialise(logging=True)


def get_match_history():
    n=0
    start_match_seq_num = 1704401237
    t0 = datetime.datetime.now()

    while n < 400:


        sleep(1.0)

        gmh = api.get_match_history_by_seq_num(start_at_match_seq_num=start_match_seq_num,
                                               matches_requested=400)

        if gmh['status'] != 1:
            print gmh['statusDetail']

        else:
            for match in gmh['matches']:

                match_id = match['match_id']

                if db.coll.find_one({'match_id':match_id}) != None:
#                 logger.debug('Encountered match %s already in database, exiting.' % match_id)
                    print '.',
                    #exit(0)

                else:
                    sleep(1.0)

                    db.coll.insert(match)

        last_match_seq_num = gmh['matches'][-1]['match_seq_num']
        # logger.debug('Match_id of last match of GMH query: %s' % last_match_id)
        # We don't want to record the last match twice, so subtract 1
        start_match_seq_num = last_match_seq_num + 1
        n+=1
        t1 = datetime.datetime.now()
        delta_t = str(t1 - t0)
        print "Process {0} request use time: {1}".format(n, delta_t)

if __name__ == '__main__':

    get_match_history()
