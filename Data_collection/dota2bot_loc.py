import os #, logging, argparse
import dota2api
# from util import get_game_mode_string
from pymongo import MongoClient
from time import sleep
from sys import exit
import datetime
import json
import pdb

filename = 'match_history.json'

#set up dota2api

api = dota2api.Initialise(logging=True)

def check_time():
    t1 = datetime.datetime.now()
    delta_t = str(t1 - t0)
    return delta_t

def check_date(t):
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')

'''
def check_last_insert_match(file):

    with open(file, 'r') as f:
        current_req_num = sum(1 for _ in f)
        start_match_seq_num = 0

        if current_req_num == 0:
            start_match_seq_num = 1704401237
        else:
            for line in f:
                last = json.loads(line)
                start_match_seq_num = last['matches'][-1]['match_seq_num'] + 1

    return current_req_num, start_match_seq_num
'''

def get_match_history():

    n=0
    start_match_seq_num = 1704401237

    # pdb.set_trace()

    while n < 300:


        sleep(1.0)
        try:

            gmh = api.get_match_history_by_seq_num(start_at_match_seq_num=start_match_seq_num)

            if gmh['status'] != 1:
                print gmh['statusDetail']

            else:
                sleep(1.0)

                with open('match_history.json', mode='a') as feedsjson:
                    json.dump(gmh, feedsjson)
                    feedsjson.write('\n')

            last_match_seq_num = gmh['matches'][-1]['match_seq_num']
            start_match_seq_num = last_match_seq_num + 1

            n+=1
            if n % 100 == 0:
                sleep(10.0)
                with open('match_history_log.txt', mode='a') as check:
                    check.write("Process {0} request use time: {1}\n".format(n, check_time()))

        except:
            print 'error'
            continue

    date=gmh['matches'][-1]['start_time']
    with open('match_history_log.txt', mode='a') as check:
        check.write("Next Seq_Num:{0}, Current Match Date:{1} \n"
                    .format(start_match_seq_num, check_date(date)))


if __name__ == '__main__':
    t0 = datetime.datetime.now()
    get_match_history()
