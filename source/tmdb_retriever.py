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
import concurrent.futures
import requests

api_key = config.tmdb_api_key
dataset_path = "../data/processed/final_dataset.tsv"
path = pd.read_csv(dataset_path)

output = []
CONNECTIONS = 60
TIMEOUT = 8
index_final = 0

def urls_tmdb():
    return ['https://api.themoviedb.org/3/find/' + i + '?api_key=' +  api_key + '&external_source=imdb_id' for i in path.tconst]

def request_tmdb(url, timeout):
    request = requests.get(url, timeout=timeout)
    return request.json()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(request_tmdb, url, TIMEOUT) for url in urls_tmdb())
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            output.append(data)

df = pd.DataFrame({"column": output})
df.to_csv("final1.csv")
