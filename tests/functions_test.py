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
