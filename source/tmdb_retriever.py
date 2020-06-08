#!/usr/bin/env python3
# coding: utf-8
import requests
import config as config
import constants as constants
import pandas as pd
import json
import concurrent.futures
import time

output = []
CONNECTIONS = 40
TIMEOUT = 5

title_basics_df = pd.read_csv("../data/processed/dataset_builder/title_basics_before_2020.csv", engine="python")

urls = [constants.BASE_URL + 'find/' + i + '?api_key=' +  config.tmdb_api_key + '&external_source=imdb_id' for i in title_basics_df.tconst]

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
            print(str(len(output)))
    time_2 = time.time()

print(f'Took {time_2-time_1:.2f} s')

with open('../data/processed/json/tmdb_id_list.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
