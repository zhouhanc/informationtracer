import requests
import pandas as pd
from datetime import date, timedelta
import time
from pprint import pprint
import json
import os

SUBMIT_URL = 'https://informationtracer.com/submit'
STATUS_URL = 'https://informationtracer.com/status'
RESULT_URL = 'https://informationtracer.com/result'

# STEP 1: submit a search query, and get id_hash256 (a unique identifier)
def step_1_submit(query, token, start_date, end_date):
    """
    query: string
    token: string
    start_date: string in format yyyy-mm-dd
    end_date: string in format yyyy-mm-dd
    twitter_sort_by: 'engagement' or 'time'
    """    
    id_hash256 = None
    try:
        response = requests.post(SUBMIT_URL, 
                             timeout=10,
                             json={'query': query, 
                                   'token': token,
                                   'start_date': start_date,
                                   'end_date': end_date,
                                   'twitter_sort_by': 'engagement'
                                   }                                   
                            )
        if 'id_hash256' in response.json():
            id_hash256 = response.json()['id_hash256']
        else:
            print("Submission failed!")
            print(response.json())

    except Exception as e:
        print("Submission failed!")
        print(e)
    
    return id_hash256
        

# STEP 2: periodically check status, and get partial results (first 5 tweets)
def step_2_check_status(id_hash256, token):
    task_status = None
    MAX_ROUND = 40
    current_round = 0

    while task_status != 'finished' and  current_round < MAX_ROUND:            
        current_round += 1
        print(current_round)
        try:
            full_url = '{}?id_hash256={}&token={}'.format(
                STATUS_URL, id_hash256, token
                )
            response = requests.get(full_url, timeout=10).json()            
            print(response)
            if 'status' in response:
                # NOTE: can render status_percentage, status_text on the UI
                task_status = response['status']
                status = response['status']
                status_percentage = response['status_percentage']
                status_text = response['status_text']
                tweet_preview = response.get('tweet_preview', None)
                if tweet_preview:
                    # NOTE: can render tweet_preview on the UI            
                    print('received {} partial tweets'.format(len(tweet_preview)))

                if status != 'finished':
                    time.sleep(6)
                else:
                    return 'finished'

            else:
                print('status is not in response')
                pprint(response)
                return 'failed'

        except Exception as e:
            print('Exception when checking job status!')
            print(e)

    return 'timeout'


# STEP 3: get result (well-formatted result per platform)
def step_3_get_result_by_platform(source, id_hash256, token):    
    try:
        url = 'https://informationtracer.com/download?source={}&type=csv&id={}&token={}'.format(source, id_hash256, token)
        df = pd.read_csv(url)
        return df
    except Exception as e:
        print(e)

    return []


# DEPRECATED
# STEP 3: get result (aggregated, minimized payload and extra intelligence)
def step_3_get_result_aggregated(id_hash256, token):
    try:
        response = requests.get('{}?token={}&id_hash256={}'.format(RESULT_URL, token, id_hash256), timeout=10)
        pprint(response.json().keys())
        return response.json()
    except Exception as e:
        print(e)

    return []


if __name__ == '__main__':
    query = 'nvidia AND stock'
    token = 'XXX'
    start_date = '2023-11-03'
    end_date = '2023-11-06'

    id_hash256 = step_1_submit(query, token, start_date, end_date)
    if id_hash256:
        print(id_hash256)
        status = step_2_check_status(id_hash256, token)
        print(status)
        if status == 'finished':
            # get twitter posts
            result = step_3_get_result_by_platform('twitter', id_hash256, token)
            print(result)
            # NOTE: do something with result
            # ....




