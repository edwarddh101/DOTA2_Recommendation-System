import os, logging, sys
import dota2api
import datetime
import json
import pdb
from time import sleep
import random

## Need to move the global variable to set up function

t0 = datetime.datetime.now()
filename = 'match_history_sample.json'
initial_req_num = 0
initial_seq_num = 1704401237
initial_date = datetime.datetime(2015, 11, 11, 0)
last_match_date = datetime.datetime(2015, 12, 16, 0)

#set up dota2api
api = dota2api.Initialise(logging=True)

def setup():
    '''
    Set up dota2 api and show current status
    '''
    n = check_next_insert_match(filename)[0]
    if n == 0:
        pass
    else:
        n -= 1
    log_time(n)


def log_time(n):
    '''
    INPUT: INT, JSON: Total Request Number
    OUTPUT: NONE
    '''
    t1 = datetime.datetime.now()
    delta_t = str(t1 - t0)
    # n = check_last_insert_match(filename)[0]
    with open('match_history_log.txt', mode='a') as check:
        check.write("Current Request: {0}, Current time: {1}, Running time: {2}\n"
                    .format(n, t1, delta_t))

def log_match_info(gmh):
    '''
    INPUT: JSON
    OUTPUT: NONE
    '''
    current_match_seq_num, current_match_date = check_current_match_info(gmh)
    date = datetime.datetime.fromtimestamp(current_match_date)

    with open('match_history_log.txt', mode='a') as check:
        check.write("Current Seq_Num:{0}, Current Match Date:{1} \n"
                    .format(current_match_seq_num, date))

def check_current_match_info(gmh):
    '''
    INPUT: JSON object, with informatin of one api request
    OUTPUT: TUPLE, current sequence number, current date
    '''
    current_match_seq_num = gmh['matches'][-1]['match_seq_num']
    current_match_date = gmh['matches'][-1]['start_time']
    return current_match_seq_num, current_match_date


def check_next_insert_match(file):

    start_req_num = 0
    with open(file, 'r') as f:
        ## Need to explore more efficient way to check last line and tot line num.
        for line in f:
            last = json.loads(line)
            start_req_num += 1

        if start_req_num == 0:
            start_match_seq_num = initial_seq_num
            start_match_date = initial_date
        else:
            start_match_seq_num = check_current_match_info(last)[0]+1
            start_match_date_unix = check_current_match_info(last)[1]+1
            start_match_date = datetime.datetime.fromtimestamp(start_match_date_unix)

    return start_req_num, start_match_seq_num, start_match_date

def get_match_history(start_match_seq_num):

    gmh = api.get_match_history_by_seq_num(start_at_match_seq_num=start_match_seq_num)

    if gmh['status'] != 1:
        print gmh['statusDetail']
    else:
        sleep(2.0)
        with open(filename, mode='a') as feedsjson:
            json.dump(gmh, feedsjson)
            feedsjson.write('\n')
    return gmh


def main():
    n, start_match_seq_num, start_match_date = check_next_insert_match(filename)

    while start_match_date < last_match_date:
        sleep(2.0)
        try:
            gmh = get_match_history(start_match_seq_num)
# Add random number after 38,000 request intent to get 1/20 data
            start_match_seq_num = check_current_match_info(gmh)[0] + random.randint(1,4000)

        except:
            e = sys.exc_info()[0]
            with open('error_message.txt', 'a') as f:
                f.write("error:{0} \n".format(e))

            sleep(30.0)
            continue

        n+=1
        if n % 1000 == 0:
            sleep(5400.0)
            log_time(n)
            log_match_info(gmh)

    log_match_info(gmh)

if __name__ == '__main__':
    setup()
    main()
