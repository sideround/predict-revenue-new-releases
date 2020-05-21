#!/usr/bin/env python3
# coding: utf-8
import requests
import source.config as config
import source.constants as constants
import pandas as pd
import os.path

api_key = config.tmdb_api_key
dataset_path = "./data/processed/final_dataset.tsv"

class Tmdb_Parser(object):

    def __init__(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.path = os.path.join(my_path, "./data/processed/final_dataset.tsv")

    def retrieve_dataset(self):
        return pd.read_csv(dataset_path)

    def get_imdb_keys(self):
        dataset = pd.read_csv(dataset_path)
        return dataset.tconst

    def create_dataframe_from_list(self, keys, path = dataset_path):
        if isinstance(keys, list):
            dataset = pd.read_csv(path, sep='\n')
            if len(dataset) == len(keys):
                series =  pd.Series(keys)
                dataset['TMDBId'] = series
                return dataset
            else:
                raise Exception("List has not the same length as the dataset")
            return keys
        else:
            raise Exception('You should send a list!')

    def save_csv(self, dataset, path):
        dataset.to_csv(path)

# async def diss(lis):
#   x = []
#   index = 0
#   for column in lis:
#       response = requests.get('https://api.themoviedb.org/3/find/' + column + '?api_key=' +  api_key + '&external_source=imdb_id')
#       highest_revenue = response.json()
#       if "movie_results" in highest_revenue:
#           if len(highest_revenue.get("movie_results")) >= 1:
#               if "id" in highest_revenue.get("movie_results")[0]:
#                   print(f"✅ Successfully got {index} item, {round((index * 100) / len(path.tconst), 3)}% completed.")
#                   index += 1
#                   x.append(highest_revenue.get("movie_results")[0]["id"])
#               else:
#                   print("🚨 Item not available: Id not found")
#           else:
#               print("🚨 Item not available: Id not found")
#       else:
#           print("🚨 Item not available: Id not found")
#   return x
#
#
# async def main():
#   lis = path.tconst
#   res = await diss(lis)
#   return res
#
# loop = asyncio.get_event_loop()
# res = loop.run_until_complete(main())
# print(res)

# for column in path.tconst:
#     response = requests.get('https://api.themoviedb.org/3/find/' + column + '?api_key=' +  api_key + '&external_source=imdb_id')
#     highest_revenue = response.json()
#     if "movie_results" in highest_revenue:
#         if len(highest_revenue.get("movie_results")) >= 1:
#             if "id" in highest_revenue.get("movie_results")[0]:
#                 print(highest_revenue.get("movie_results")[0].get("id"))
#             else:
#                 print("fallo id")
#         else:
#             print("fallo len")
#     else:
#         print("fallo movie_results")
#     print(f"vamos por el {index} de {len(path.tconst)}")
#     index += 1
