#!/usr/bin/env python3
# coding: utf-8
import requests
import config as config
import constants as constants
import pandas as pd
import os.path
import numpy as np
import asyncio
import json
from imdb import IMDb
import csv

import pandas as pd
import concurrent.futures
import requests
import time

api_key = config.tmdb_api_key

output = []
CONNECTIONS = 60
TIMEOUT = 8

tmdb_id_list = pd.read_csv("../data/processed/tmdb_ids.csv", engine="python")

urls = ['https://api.themoviedb.org/3/movie/' + str(i) + '?api_key=' +  api_key + '&append_to_response=credits' for i in tmdb_id_list.tmdb_id]

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
with open('../data/processed/json/tmdb_movie_list.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
