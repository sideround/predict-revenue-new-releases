#!/usr/bin/env python3
from source.tmdb_retriever import *
import pytest
import numpy as np
import os.path

"""
Check dataset used on tmdb_retriever is the final one
"""
def test_dataset_connection():
    parser = Tmdb_Parser()
    my_path = os.path.abspath(os.path.dirname(__file__))
    dataset_mock = pd.read_csv("./data/processed/final_dataset.tsv")
    assert parser.retrieve_dataset().equals(dataset_mock)
"""

"""
def test_request_response():
    # Send a request to the API server and store the response.
    response = requests.get('https://api.themoviedb.org/3/find/tt9390218?api_key=1914255fc1f88bfdffb5f0af5f64a5e2&external_source=imdb_id')

    # Confirm that the request-response cycle completed successfully.
    assert response.ok == True

def test_imdb_keys_successful():
    parser = Tmdb_Parser()
    assert list(parser.get_imdb_keys()[:5]) == ["tt0015724", "tt0016906", "tt0035423", "tt0036606", "tt0057461"]

# def test_save_csv_correct_dataset():
#      parser = Tmdb_Parser()
#      successful_list = list(range(0, 50))
#      dataset_mock = pd.read_csv("data/final_dataset_mock_with_tmdb.csv", sep='\t')
#      sup = parser.create_dataframe_from_list(successful_list, "data/final_dataset_mock_without_tmdb.csv")
#
#      sup.to_csv("sup.csv")
#      dataset_mock.to_csv("mock.csv")
#
#      assert parser.create_dataframe_from_list(successful_list, "data/final_dataset_mock_without_tmdb.csv").equals(dataset_mock)

def test_save_csv_incorrect_length():
    parser = Tmdb_Parser()
    with pytest.raises(Exception):
        assert parser.create_dataframe_from_list([1212, 1212, np.NaN], "data/final_dataset_mock.csv")

def test_save_incorrect_type():
    parser = Tmdb_Parser()
    with pytest.raises(Exception):
        parser.create_dataframe_from_list(1212)
