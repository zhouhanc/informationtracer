import requests
from datetime import date, timedelta
import time
from pprint import pprint
import json
import os

TRACE_URL = 'https://informationtracer.com/api/v1/submit'
RESULT_URL = 'https://informationtracer.com/api/v1/result'
JOB_STATUS_URL = 'https://informationtracer.com/job_status'

def trace(query=None, skip_result=False, result_filename=None, 
    timeout=240, verbose=True, token=None, start_date=None, end_date=None):
    """
        Submit a query, wait for the job to finish, and collect the results
        
        Return: id_hash256 (unique id of the search)
    """
    if query is None:
        print('query cannot be none')
        return

    # by default, start_date is 7 days ago, end_date is today+1
    collect_date=date.today()

    if start_date is None:
        start_date = collect_date - timedelta(days=7)
        start_date = str(start_date)    

    if end_date is None:
        end_date = collect_date + timedelta(days=1)
        end_date = str(end_date)

    response = requests.post(TRACE_URL, 
                             json={'query': query, 
                                   'token': token,
                                   'start_date': start_date,
                                   'end_date': end_date
                                   }                                   
                                   )
    
    pprint(response.json())
    if 'error' in response.json():  
        print('error when submitting the query.')          
        return

    task_status = None    
    start = time.time()
    end = time.time()
    job_id = response.json()['job_id']
    id_hash256 = None

    while task_status != 'finished' and int(end - start) <= timeout:
        full_url = '{}/{}'.format(JOB_STATUS_URL, job_id)
        # TODO: add try catch in case of connection error (Connection aborted)

        try:
            response = requests.get(full_url)
            meta_data = response.json()['data']['task_meta']
            if 'id_hash256' in meta_data:
                id_hash256 = meta_data['id_hash256']

            print('{} seconds passed...'.format(int(end - start)))
            if verbose:
                pprint(response.json()['data'])
                
            task_status = response.json()['data']['task_status']

            if task_status == 'failed':
                print('task status is failed. for your reference, id_hash256 is {}'.format(id_hash256))
                return 

            if task_status != 'finished':
                time.sleep(5)
            end = time.time()

        except Exception as e:
            print(e)
            print('Get exception when checking job status. Abort current task.')
            break


    if task_status == 'finished':
        meta_data = response.json()['data']['task_meta']
        id_hash256 = meta_data['id_hash256']
        print('colleciton finished!')
    else:
        print('timeout. for your reference, id_hash256 is {}'.format(id_hash256))
        return 

    if id_hash256 is None:
        print('cannot get result, missing id_hash256')
        return 

    if skip_result: return id_hash256

    response = requests.get('{}?token={}&id_hash256={}'.format(RESULT_URL, token, id_hash256))

    if verbose:
        pprint(response.json())
    if result_filename:
        json.dump(response.json(), open(result_filename, 'w'), indent=4)
    else:
        json.dump(response.json(), open('result_{}.json'.format(id_hash256), 'w'), indent=4)
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='search parameters.')
    parser.add_argument('--query', type=str, default=None, help='search string')
    parser.add_argument('--start_date', type=str, default=None, help='earlist post, format YYYY-MM-DD')
    parser.add_argument('--end_date', type=str, default=None, help='latest post, format YYYY-MM-DD')
    parser.add_argument('--token', type=str, required=True, help='API token')
    parser.add_argument('--skip_result', action='store_true', default=False, required=False, help='if exists, skip collecting results')
    parser.add_argument('--timeout', type=int, default=240)
    parser.add_argument('--result_filename', type=str, default=None,
                       help='filename to store result json file (absolute path)')

    args = parser.parse_args()
    if args.query is None:
        print('must specify a query (--query "XYZ")')
        exit(0)

    trace(query=args.query,
        token=args.token,
        start_date=args.start_date,
        end_date=args.end_date,
        timeout=args.timeout,
        skip_result=args.skip_result,
        result_filename=args.result_filename)





