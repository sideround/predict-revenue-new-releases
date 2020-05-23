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

api_key = config.tmdb_api_key
dataset_path = "./final_tmdb.csv"
path = pd.read_csv(dataset_path)
print(path)
import pandas as pd
import concurrent.futures
import requests
import time

out = []
CONNECTIONS = 60
TIMEOUT = 8
index_final = 0

urls = ['https://api.themoviedb.org/3/movie/' + i + '?api_key=' +  api_key + '' for i in path.tmdb_key]
print(urls)
def load_url(url, timeout):
    ans = requests.get(url, timeout=timeout)
    return ans.json()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
    time1 = time.time()
    print(future_to_url)
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            out.append(data)
            print(str(len(out)),end="\r")

    time2 = time.time()

print(f'Took {time2-time1:.2f} s')
print(out)

import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=4)
