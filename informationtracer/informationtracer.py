import requests
import time
from pprint import pprint
import json
import os

TRACE_URL = 'https://informationtracer.com/api/v1/submit'
RESULT_URL = 'https://informationtracer.com/api/v1/result'

def trace(keyword=None, output_dir=None, 
    output_filename=None, input_filename=None, 
    timeout=180, is_async=False, no_print=False, token=None):
    """
        Submit a keyword, wait for the job to finish, and collect the results

        Preference: input_filename > keyword
    """
    if keyword is None and input_filename is None:
        print('NOTE: must specify a keyword or an input_filename')
        return

    if input_filename:
        # read queries one by one
        with open(input_filename, 'r') as f_in:
            keywords = [line.strip() for line in f_in]
    else:
        if isinstance(keyword, str):
            keywords = [keyword]
        else:
            keywords = keyword

    # keywords is a list of keyword
    for term in keywords:
        response = requests.post(TRACE_URL, 
                                 json={'term': term, 
                                       'token': token}
                                       )
        pprint(response.json())
        if 'error' in response.json():            
            return

        task_status = None    
        start = time.time()
        end = time.time()
        job_id = response.json()['job_id']

        while task_status != 'finished' and int(end - start) <= timeout:
            full_url = 'https://informationtracer.com/jobs/{}'.format(job_id)
            # TODO: add try catch in case of connection error (Connection aborted)
            response = requests.get(full_url)
            # print(response.status_code)
            pprint(response.json()['data']['tast_meta'])
            print('{} seconds passed...'.format(int(end - start)))
            task_status = response.json()['data']['task_status']
            if task_status != 'finished':
                time.sleep(1)
            end = time.time()

        if task_status == 'finished':
            print('colleciton finished!')
        else:
            print('timeout, collection not finished!')

        response = requests.post(RESULT_URL, 
                                json={'term': term, 
                                       'token': token}
                                )

        if output_dir:
            # create dir if not exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

        if output_dir is None and output_filename is None:
            pprint(response.json())
            print('=============printing results to the stdout=================')
        elif output_filename is not None:
            json.dump(response.json(), open(output_filename, 'w'), indent=4)            
            print('=============writing results to file =================')
        else:
            json.dump(response.json(), open(output_dir + '/' +  str(job_id) + '_result.json', 'w'), indent=4)
            print('=============writing results to file =================')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='search parameters.')
    parser.add_argument('--keyword', type=str, default=None, help='keyword to search, can be a string or a list of string')
    parser.add_argument('--token', type=str, required=True, help='API token')
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('--output_dir', type=str, default=None,
                       help='directory to save result file')
    parser.add_argument('--output_filename', type=str, default=None,
                       help='absolute filename of result file')                           
    parser.add_argument('--input_filename', type=str, default=None,
                       help='if you have multiple keywords to search, we will read them from a text file, where each line is a keyword')                                   
    parser.add_argument('--is_async', action='store_true', default=False,
                       help='whether to collect in an async way (a separate process)')

    args = parser.parse_args()
    if args.keyword is None and args.input_filename is None:
        print('must specify a keyword (--keyword XYZ) or a filename (--input_filename XYZ.txt)')        
        exit(0)

    trace(keyword=args.keyword,
        keyword_list=args.keyword_list,
        output_dir=args.output_dir, 
        output_filename=args.output_filename, 
        input_filename=args.input_filename,
        token=args.token,
        timeout=args.timeout,
        is_async=args.is_async)





