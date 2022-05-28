import requests
import time
from pprint import pprint
import json
import os

TRACE_URL = 'https://informationtracer.com/api/v1/submit'
RESULT_URL = 'https://informationtracer.com/api/v1/result'

def trace(term=None, output_dir=None, 
    output_filename=None, input_filename=None, 
    timeout=180, is_async=False, no_print=False, token=None):
    """
        Submit a term, wait for the job to finish, and collect the results
    """
    if term is None and input_filename is None:
        print('NOTE: must specify a term or an input_filename')
        return

    if input_filename:
        # read queries one by one
        with open(input_filename, 'r') as f_in:
            terms = [line.strip() for line in f_in]
    else:
        terms = [term]

    for term in terms:
        response = requests.post(TRACE_URL, 
                                 json={'term': term, 
                                       'token': token}
                                       )
        pprint(response.json())
        if 'error' in response.json():            
            exit(1)

        task_status = None    
        start = time.time()
        end = time.time()
        job_id = response.json()['job_id']

        while task_status != 'finished' and int(end - start) <= timeout:
            full_url = 'https://informationtracer.com/jobs/{}'.format(job_id)
            response = requests.get(full_url)
            # print(response.status_code)
            pprint(response.json()['data']['tast_meta'])
            print('{} seconds passed...'.format(int(end - start)))
            task_status = response.json()['data']['task_status']
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
        elif output_filename is not None:
            json.dump(response.json(), open(output_filename, 'w'), indent=4)
        else:
            json.dump(response.json(), open(output_dir + '/' +  str(job_id) + '_result.json', 'w'), indent=4)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='search parameters.')
    parser.add_argument('--term', type=str, default=None, help='term to search')
    parser.add_argument('--token', type=str, required=True, help='API token')
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('--output_dir', type=str, default=None,
                       help='directory to save result file')
    parser.add_argument('--output_filename', type=str, default=None,
                       help='absolute filename of result file')                           
    parser.add_argument('--input_filename', type=str, default=None,
                       help='if you have multiple terms to search, we will read them from a text file, where each line is a term')                                   
    parser.add_argument('--is_async', action='store_true', default=False,
                       help='whether to collect in an async way (a separate process)')

    args = parser.parse_args()
    if args.term is None and args.input_filename is None:
        print('must specify a term (--term XYZ) or a filename (--input_filename XYZ.txt)')
        exit(0)

    trace(term=args.term, 
        output_dir=args.output_dir, 
        output_filename=args.output_filename, 
        input_filename=args.input_filename,
        token=args.token,
        timeout=args.timeout,
        is_async=args.is_async)





