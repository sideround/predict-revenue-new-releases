#!/usr/bin/env python3
# coding: utf-8
import config as config
import constants as constants
import numpy as np
import json
import pandas as pd
import concurrent.futures
import requests
import time

output = []
CONNECTIONS = 60
TIMEOUT = 8

tmdb_cast_list = pd.read_csv("../data/processed/people_transformation/cast_ids.csv", engine="python")

urls = [constants.BASE_URL + 'person/' + str(i) + '/movie_credits?api_key=' +  config.tmdb_api_key + '&append_to_response=credits' for i in tmdb_cast_list.cast_id]

def request_tmdb(url, timeout):
    request = requests.get(url, timeout=timeout)
    return request.json()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(request_tmdb, url, TIMEOUT) for url in urls)
    time_1 = time.time()
    print(future_to_url)
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            output.append(data)
            print(str(len(output)),end="\r")
    time_2 = time.time()

print(f'Took {time_2-time_1:.2f} s')

import json
with open('../data/processed/json/tmdb_crew_list.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
